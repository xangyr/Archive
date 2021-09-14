module guessing(number, in_number, isGuess, state);

	input [3:0]number;
	input [3:0]in_number;
	input isGuess;
	output reg [2:0]state;

always @(*) 
begin
if(isGuess == 1)
	begin
		if(in_number[3] == ~number[3])
		begin
			state = 3'b100;
		end
		else if(in_number[2] == ~number[2])
		begin
			state = 3'b011;
		end
		else if(in_number[1] == ~number[1])
		begin
			state = 3'b010;
		end	
		else if(in_number[0] == ~number[0])
		begin
			state = 3'b001;
		end
		else 
		begin
			state = 3'b000;
		end
	end
end
endmodule