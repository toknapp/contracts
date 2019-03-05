OUT=build

all: $(OUT)/Coin.bin $(OUT)/Forward.bin $(OUT)/Echo.bin $(OUT)/State.bin $(OUT)/further.bin

%: $(OUT)/%.bin

$(OUT)/%.bin: %.sol
	solc --optimize --overwrite -o $(OUT) --abi --hashes --bin $<

$(OUT)/%.bin: %.evm
	mkdir -p $(basename $@)
	./as-evm <$< >$@

clean:
	rm -rf $(OUT)

.PHONY: clean all
