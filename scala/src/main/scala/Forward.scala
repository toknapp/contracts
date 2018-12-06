package co.upvest.contracts

import co.upvest.dry.essentials._
import co.upvest.dry.cryptoadt.ethereum.{Address, Wei, Wallet}
import co.upvest.dry.web3jz.Web3jz
import co.upvest.dry.web3jz.abi.{Arg, functionSelector}

import cats.syntax.option._

import scala.concurrent.{Future, ExecutionContext}

case class Forward(contract: Address) {

  def forward(web3jz: Web3jz)(
    originator: Wallet,
    target: Address,
    value: Wei,
    input: Bytes
  )(implicit ec: ExecutionContext): Future[Unit] = for {
    gp <- web3jz.gasPrice()
    n <- web3jz.nonce(originator)
    tx = web3jz.sign(
      originator,
      to = contract,
      value = Wei.Zero,
      gasPrice = gp,
      gasLimit = NonNegativeBigInt(100000).get, // TODO: make configurable
      nonce = n,
      input = Forward.input.forward(target, value, input).some
    )
    _ <- web3jz.submit(tx)
  } yield ()


    Future successful true
}

object Forward {
  object input {
    def forward(target: Address, value: Wei, input: Bytes): Bytes =
      functionSelector("forward(address,uint256,bytes)") ++
        Arg.encode((target, value, input))
  }
}
