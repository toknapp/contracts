OUT=build

all: $(OUT)/Coin.bin $(OUT)/Forward.bin $(OUT)/Echo.bin $(OUT)/State.bin $(OUT)/further.bin

$(OUT)/%.bin: %.sol
	solc --optimize --overwrite -o $(OUT) --asm --abi --hashes --bin $<

$(OUT)/%.bin: $(OUT)/%.body.bin $(OUT)/%.init.bin boot.evm
	./ld-evm $^ >$@

$(OUT)/%.bin: %.evm
	mkdir -p $(basename $@)
	./as-evm <$< >$@

clean:
	rm -rf $(OUT)

.PHONY: clean all
.PRECIOUS: $(OUT)/%.bin
