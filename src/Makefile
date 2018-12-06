OUT=build

all: $(OUT)/Coin.bin $(OUT)/Forward.bin $(OUT)/Echo.bin

%: $(OUT)/%.bin

$(OUT)/%.bin: %.sol
	solc --optimize --overwrite -o $(OUT) --abi --hashes --bin $<

clean:
	rm -rf $(OUT)

.PHONY: clean all
