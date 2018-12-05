package co.upvest.contracts

import org.scalatest.{WordSpec, Matchers}
import org.scalatest.concurrent.{ScalaFutures, IntegrationPatience}
import org.scalatest.prop.GeneratorDrivenPropertyChecks

import co.upvest.dry.essentials._
import co.upvest.dry.cryptoadt.ethereum.{Address, Wei}
import co.upvest.dry.catz.syntax._
import co.upvest.dry.test.ArbitraryUtils
import co.upvest.dry.cryptoadt.ArbitraryInstances
import co.upvest.dry.web3jz.Fees

import cats.instances.list._
import cats.syntax.option._

import scala.concurrent.ExecutionContext.Implicits.global

import TestUtils.{web3jz, Faucet, WeiRange, accountIsEmpty, loadContractBinary}

class Basics extends WordSpec
  with Matchers with ScalaFutures with GeneratorDrivenPropertyChecks
  with ArbitraryInstances with IntegrationPatience with ArbitraryUtils {

  "the TestUtils.faucets" should {
    "have a non-negative balance" in {
      TestUtils.faucets >>| { _.address } >>| { a =>
        whenReady(web3jz balance a) { _ should not be Wei.Zero }
      }
    }

    "be able to deploy a contract" in {
      val f = pick[Faucet]
      val data = loadContractBinary("Echo")
      whenReady(
        for {
          gp <- web3jz.gasPrice()
          n <- web3jz.nonce(f)
          (tx, a) = web3jz.contract(
            f,
            value = Wei.Zero,
            gasPrice = gp,
            gasLimit =
              Fees.TxCreate + Fees.Transaction + Fees.codeDeposit(data) +
                NonNegativeBigInt(6500).get, // TODO: would it be possible to get an exact value here?
            nonce = n,
            data
          )
          c0 <- web3jz.code(a)
          _ <- web3jz.submit(tx)
          c1 <- web3jz.code(a)
        } yield (c0, c1)
      ) { case (c0, c1) =>
        c0 shouldBe Array[Byte](0) // TODO: wth? how can one then differentiate between a contract without code and code == [0]?
        c1 should not be empty
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
                input = none
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
