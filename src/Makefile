OUT=build

all: $(OUT)/Coin.bin $(OUT)/Forward.bin

%: $(OUT)/%.bin

$(OUT)/%.bin: %.sol
	solc --overwrite -o $(OUT) --abi --hashes --bin $<

clean:
	rm -rf $(OUT)

.PHONY: clean all
