package co.upvest.contracts

import org.scalatest.{WordSpec, Matchers}
import org.scalatest.concurrent.{ScalaFutures, IntegrationPatience}

import co.upvest.dry.essentials._
import co.upvest.dry.test.ArbitraryUtils
import co.upvest.dry.cryptoadt.ethereum.{Wei, Wallet}

import scala.concurrent.Future
import scala.concurrent.ExecutionContext.Implicits.global

import TestUtils.{loadContractBinary, web3jz, Faucet}

class ERC20Spec extends WordSpec
  with Matchers with ScalaFutures with ArbitraryUtils with IntegrationPatience {

  def freshCoin(w: Wallet): Future[ERC20] = for {
    gp <- web3jz.gasPrice()
    n <- web3jz.nonce(w)
    (tx, a) = web3jz.contract(
      w,
      value = Wei.Zero,
      gasPrice = gp,
      gasLimit = NonNegativeBigInt(2000000).get,
      nonce = n,
      loadContractBinary("Coin")
    )
    _ <- web3jz.submit(tx)
  } yield ERC20(a)

  "ERC20" should {
    "deploy contract and receive the total supply" in {
      val f = pick[Faucet]
      whenReady(
        for {
          c <- freshCoin(f)
          b <- c.balance(web3jz)(f)
          ts <- c.totalSupply(web3jz)
        } yield (b, ts)
      ) { case (b, totalSupply) => b shouldBe totalSupply }
    }
  }
}
