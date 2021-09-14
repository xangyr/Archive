//send the boards 50MHz clock to this and on the output will be 1Hz clock
module clock_divider(clk_50MHz, state, clk_new);
	
	input clk_50MHz;
	input [2:0]state;
	output reg clk_new;

	reg [27:0] counter = 0;
	
	reg [27:0] counter_goal;
	

	
	always@(posedge clk_50MHz)
	begin
	case (state)
		3'b001 : counter_goal = 28'd3_125_000;
		3'b010 : counter_goal = 28'd6_250_000;
		3'b011 : counter_goal = 28'd12_500_000;
		3'b100 : counter_goal = 28'd25_000_000;
		default : counter_goal = 28'd1;
	endcase
		
		if(counter == counter_goal)
		begin
			counter <= counter + 1;
			clk_new <= 1;
		end else if(counter == (counter_goal*2))
		begin
			counter <= 0;
			clk_new <= 0;
		end else begin
			counter <= counter + 1;
			clk_new <= clk_new;
		end
	end
endmodule
