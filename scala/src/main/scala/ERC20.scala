package co.upvest.contracts

import co.upvest.dry.essentials._
import co.upvest.dry.cryptoadt.ethereum.{Address, UInt256, Wallet, Wei}

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

  def transfer(web3jz: Web3jz)(
    from: Wallet,
    to: Address,
    amount: Token
  )(implicit
    ec: ExecutionContext
  ): Future[Unit] = for {
    gp <- web3jz.gasPrice()
    n <- web3jz.nonce(from)
    tx = web3jz.sign(
      from,
      to = contract,
      value = Wei.Zero,
      gasPrice = gp,
      gasLimit = NonNegativeBigInt(51241).get, // TODO: make configurable
      nonce = n,
      input = input.transfer(to, amount).some
    )
    _ <- web3jz.submit(tx)
  } yield ()

  object input {
    def balance(of: Address): Bytes =
      functionSelector("balanceOf(address)") ++ Arg(of)

    val totalSupply: Bytes = functionSelector("totalSupply()")

    def transfer(to: Address, amount: Token): Bytes =
      functionSelector("transfer(address,uint256)") ++
        Arg((to, amount.amount))
  }
}

object ERC20 {
  case class Token(contract: ERC20, amount: UInt256)
}
