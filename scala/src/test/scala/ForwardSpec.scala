package co.upvest.contracts

import co.upvest.dry.essentials._
import co.upvest.dry.essentials.bytes._
import co.upvest.dry.cryptoadt.{ArbitraryInstances, secp256k1}
import co.upvest.dry.cryptoadt.ethereum.{Wei, Address, UInt256}
import co.upvest.dry.test.ArbitraryUtils

import org.scalatest.{WordSpec, Matchers}
import org.scalatest.concurrent.{ScalaFutures, IntegrationPatience}

import cats.syntax.option._

import scala.concurrent.Future
import scala.concurrent.ExecutionContext.Implicits.global

import TestUtils.{web3jz, Faucet, freshCoin, loadContractBinary}

class ForwardSpec extends WordSpec
  with Matchers with ScalaFutures with ArbitraryUtils with IntegrationPatience
  with ArbitraryInstances {

  def freshForward(pk: secp256k1.PublicKey): Future[Forward] = for {
    gp <- web3jz.gasPrice()
    w = pick[Faucet]
    n <- web3jz.nonce(w)
    (tx, a) = web3jz.contract(
      w,
      value = Wei.Zero,
      gasPrice = gp,
      gasLimit = NonNegativeBigInt(3000000).get,
      nonce = n,
      data = Forward.data.constructor(
        loadContractBinary("Forward"),
        pk
      )
    )
    _ <- web3jz.submit(tx)
  } yield Forward(a)

  def freshTokenHolder(a: Address): Future[ERC20] = {
    val f = pick[Faucet]
    for {
      c <- freshCoin(f)
      ts <- c.totalSupply(web3jz)
      _ <- c.transfer(web3jz)(f, a, ts)
    } yield c
  }

  "Forward" should {
    "enable an account to transfer ERC20 tokens without holding ether" in {
      val owner = pick[secp256k1.PrivateKey]
      whenReady(
        for {
          f <- freshForward(owner.publicKey)
          c <- freshTokenHolder(f.contract)
          e0 <- web3jz.balance(f.contract)
          a = pick[Address]
          b0 <- c.balance(web3jz)(a)
          amount = ERC20.Token(c, UInt256(10))
          _ <- f.forward(web3jz)(
            originator = pick[Faucet],
            owner = owner,
            c.contract,
            Wei.Zero,
            ERC20.input.transfer(a, amount)
          )
          b1 <- c.balance(web3jz)(a)
        } yield (c, e0, b0, amount, b1)
      ) { case (c, e0, b0, amount, b1) =>
        e0 shouldBe Wei.Zero
        b0 shouldBe ERC20.Token(c, UInt256(0))
        b1 shouldBe amount
      }
    }

    "only allow the authorized key to forward calls" in {
      val owner = pick[secp256k1.PrivateKey]
      val adversary = pick[secp256k1.PrivateKey]
      whenReady(
        for {
          f <- freshForward(owner.publicKey)
          c <- freshTokenHolder(f.contract)
          a = pick[Address]
          amount = ERC20.Token(c, UInt256(10))
          _ <- f.forward(web3jz)(
            originator = pick[Faucet],
            owner = adversary,
            c.contract,
            Wei.Zero,
            ERC20.input.transfer(a, amount)
          ) recover {
            case t: RuntimeException if t.toString contains "invalid signature" =>
          }
          b <- c.balance(web3jz)(a)
        } yield (c, b)
      ) { case (c, b) =>
        b shouldBe ERC20.Token(c, UInt256(0))
      }
    }

    "not allow modifying the input" in {
      val owner = pick[secp256k1.PrivateKey]
      val adversary = pick[Address]
      whenReady(
        for {
          f <- freshForward(owner.publicKey)
          c <- freshTokenHolder(f.contract)
          intendedBeneficiary = pick[Address]
          amount = ERC20.Token(c, UInt256(10))
          nn <- f.nonce(web3jz)
          i = f.input.forward(
            owner = owner,
            nonce = nn,
            c.contract,
            Wei.Zero,
            ERC20.input.transfer(intendedBeneficiary, amount)
          )

          modified = i.hex.replace(
            intendedBeneficiary.toUnprefixedString,
            adversary.toUnprefixedString
          ).hex.get

          originator = pick[Faucet]
          gp <- web3jz.gasPrice()
          n <- web3jz.nonce(originator)
          tx = web3jz.sign(
            originator,
            to = f.contract,
            Wei.Zero,
            gp,
            gasLimit = NonNegativeBigInt(100000).get,
            nonce = n,
            input = modified.some
          )
          _ <- web3jz.submit(tx) recover {
            case t: RuntimeException if t.toString contains "invalid signature" =>
          }
          b <- c.balance(web3jz)(adversary)
        } yield (c, b)
      ) { case (c, b) =>
        b shouldBe ERC20.Token(c, UInt256(0))
      }
    }
  }
}
