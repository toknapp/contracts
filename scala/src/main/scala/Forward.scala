package co.upvest.contracts

import co.upvest.dry.essentials._
import co.upvest.dry.cryptoadt.secp256k1
import co.upvest.dry.cryptoadt.ethereum.{Address, Wei, Wallet}
import co.upvest.dry.web3jz.{Web3jz, sign}
import co.upvest.dry.web3jz.abi.{Arg, functionSelector}

import cats.syntax.option._

import scala.concurrent.{Future, ExecutionContext}

case class Forward(contract: Address) {

  def forward(web3jz: Web3jz)(
    originator: Wallet,
    owner: secp256k1.PrivateKey,
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
      input = Forward.input.forward(owner, target, value, input).some
    )
    _ <- web3jz.submit(tx)
  } yield ()
}

object Forward {
  object input {
    def forward(
      owner: secp256k1.PrivateKey,
      target: Address, value: Wei, input: Bytes
    ): Bytes = {
      val sig = sign(owner, "foo".getBytes)
      functionSelector("forward(uint8,bytes32,bytes32,address,uint256,bytes)") ++
        Arg.encode((sig.v, sig.r, sig.s, target, value, input))
    }
  }

  object data {
    def constructor(code: Bytes, owner: secp256k1.PublicKey): Bytes =
      code ++ Arg.encode(Address.from(owner))
  }
}
