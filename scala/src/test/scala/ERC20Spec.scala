package co.upvest.contracts

import org.scalatest.{WordSpec, Matchers}
import org.scalatest.concurrent.{ScalaFutures, IntegrationPatience}

import co.upvest.dry.essentials._
import co.upvest.dry.test.ArbitraryUtils
import co.upvest.dry.cryptoadt.ArbitraryInstances
import co.upvest.dry.cryptoadt.ethereum.{Address, UInt256}

import scala.concurrent.ExecutionContext.Implicits.global

import TestUtils.{web3jz, Faucet, freshCoin}

class ERC20Spec extends WordSpec
  with Matchers with ScalaFutures with ArbitraryUtils with IntegrationPatience
  with ArbitraryInstances {

  "ERC20" should {
    "deploy contract and receive the total supply" in {
      val f = pick[Faucet]
      whenReady(
        for {
          c <- freshCoin(f)
          ts <- c.totalSupply(web3jz)
          b <- c.balance(web3jz)(f)
        } yield (b, ts)
      ) { case (b, totalSupply) => b shouldBe totalSupply }
    }

    "transfer some tokens" in {
      val f = pick[Faucet]
      val a = pick[Address]
      whenReady(
        for {
          c <- freshCoin(f)
          ts <- c.totalSupply(web3jz)
          f0 <- c.balance(web3jz)(f)
          a0 <- c.balance(web3jz)(a)
          amount = ERC20.Token(c, UInt256(10))
          _ <- c.transfer(web3jz)(f, a, amount)
          f1 <- c.balance(web3jz)(f)
          a1 <- c.balance(web3jz)(a)
        } yield (c, ts, f0, a0, amount, f1, a1)
      ) { case (c, ts, f0, a0, amount, f1, a1) =>
        // TODO: make nice arithmetic on ERC20.Token:s
        f0 shouldBe ts
        a0 shouldBe ERC20.Token(c, UInt256(0))
        f1 shouldBe ERC20.Token(c, ts.amount - amount.amount)
        a1 shouldBe amount
      }
    }
  }
}
