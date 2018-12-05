package co.upvest.contracts

import org.scalatest.{WordSpec, Matchers}
import org.scalatest.concurrent.{ScalaFutures, IntegrationPatience}
import org.scalatest.prop.GeneratorDrivenPropertyChecks

import co.upvest.dry.cryptoadt.ethereum.{Address, Wei}
import co.upvest.dry.catz.syntax._
import co.upvest.dry.test.ArbitraryUtils
import co.upvest.dry.cryptoadt.ArbitraryInstances
import co.upvest.dry.web3jz.Fees

import cats.instances.list._
import cats.syntax.option._
import scala.concurrent.ExecutionContext.Implicits.global

import TestUtils.{web3jz, Faucet, WeiRange, accountIsEmpty}

class Basics extends WordSpec
  with Matchers with ScalaFutures with GeneratorDrivenPropertyChecks
  with ArbitraryInstances with IntegrationPatience with ArbitraryUtils {

  "the TestUtils.faucets" should {
    "have a non-negative balance" in {
      TestUtils.faucets >>| { _.address } >>| { a =>
        whenReady(web3jz balance a) { _ should not be Wei.Zero }
      }
    }
  }

  "a fresh address" should {
    "have balance zero" in {
      forAll { (a: Address) =>
        whenReady(web3jz balance a) { _ shouldBe Wei.Zero }
      }
    }

    "be able to receive some schmeckles" in {
      import WeiRange.normal
      forAll { (a: Address, f: Faucet, v: Wei) =>
        whenever(accountIsEmpty(a)) {
          whenReady(
            for {
              gp <- web3jz.gasPrice()
              n <- web3jz.nonce(f)
              tx = web3jz.sign(
                f,
                to = a,
                value = v,
                gasPrice = gp,
                gasLimit = Fees.Transaction,
                nonce = n,
                data = none
              )
              _ <- web3jz.submit(tx)
              b <- web3jz.balance(a)
            } yield b
          ) { _ shouldBe v }
        }
      }
    }
  }
}
