package co.upvest.contracts

import org.scalatest.{WordSpec, Matchers}
import org.scalatest.concurrent.{ScalaFutures, IntegrationPatience}
import org.scalatest.prop.GeneratorDrivenPropertyChecks

import co.upvest.dry.cryptoadt.ethereum.{Address, Wei}
import co.upvest.dry.catz.syntax._
import co.upvest.dry.cryptoadt.{ArbitraryInstances, secp256k1}

import cats.instances.list._

import TestUtils.web3jz

class Basics extends WordSpec
  with Matchers with ScalaFutures with GeneratorDrivenPropertyChecks
  with ArbitraryInstances with IntegrationPatience {

  "the TestUtils.pks" should {
    "have a non-negative balance" in {
      TestUtils.pks >>| { _.publicKey } >>| Address.from foreach { a =>
        whenReady(web3jz balance a) { _ should not be Wei.Zero }
      }
    }
  }

  "a fresh address" should {
    "have balance zero" in {
      forAll { (p: secp256k1.PublicKey) =>
        whenReady(web3jz balance Address.from(p)) { _ shouldBe Wei.Zero }
      }
    }
  }
}
