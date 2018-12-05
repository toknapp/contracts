package co.upvest.contracts

import co.upvest.dry.essentials._
import co.upvest.dry.cryptoadt.ethereum.{Address, UInt256}

import co.upvest.dry.web3jz.Web3jz
import co.upvest.dry.web3jz.abi.{Arg, functionSelector}

import cats.syntax.option._

import scala.concurrent.{Future, ExecutionContext}

case class ERC20(contract: Address) {
  import ERC20._

  def balance(web3jz: Web3jz)(of: Address)(implicit
    ec: ExecutionContext
  ): Future[Token] = web3jz.call(
    to = contract,
    input = input.balance(of).some
  ) map UInt256.apply map { Token(this, _) }

  def totalSupply(web3jz: Web3jz)(implicit
    ec: ExecutionContext
  ): Future[Token] = web3jz.call(
    to = contract,
    input = input.totalSupply.some
  ) map UInt256.apply map { Token(this, _) }

  object input {
    def balance(of: Address): Bytes =
      functionSelector("balanceOf(address)") ++ Arg(of)

    val totalSupply: Bytes = functionSelector("totalSupply()")
  }
}

object ERC20 {
  case class Token(contract: ERC20, amount: UInt256)
}
