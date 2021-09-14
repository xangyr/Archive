module guessing_game(isGuess, enable, clk, number, led);

	input isGuess;
	input enable;
	input clk;
	input [3:0] number;
	output reg led;
	
	reg [3:0]store_number;
	wire [2:0]state;
	wire new_clk;
	
guessing fun1(store_number, number, isGuess, state);
clock_divider fun2(clk, state, new_clk);
	
always @(posedge clk)
begin
	if(isGuess == 0)
	begin
		led = 0;
	end
	else if(state == 0)
	begin
		led = 1;
	end
	else
	begin
		led = new_clk;
	end
end


always @(*) 
begin
	if(isGuess == 0 && enable == 1)
	begin
		store_number = number;
	end
end
endmodule
		