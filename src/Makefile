OUT=build

CONTRACTS=Coin Forward Echo State bare_metal further

all: $(foreach c,$(CONTRACTS),$(OUT)/$c.bin)

$(OUT)/%.bin: %.sol
	solc --optimize --overwrite -o $(OUT) --asm --abi --hashes --bin $<

$(OUT)/%.bin: $(OUT)/%.runtime.bin $(OUT)/%.init.bin boot.evm
	./ld-evm $^ >$@

$(OUT)/%.bin: %.evm | $(OUT)
	./as-evm <$< >$@

$(OUT):
	mkdir -p $@

clean:
	rm -rf $(OUT)

.PHONY: clean all
.PRECIOUS: $(OUT)/%.bin
