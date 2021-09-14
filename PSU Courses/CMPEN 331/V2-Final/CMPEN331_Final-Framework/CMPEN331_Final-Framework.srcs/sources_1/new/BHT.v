`timescale 1ns / 1ps

module BHT(
    input clk,
    input [31:0] PC,
    output Prediction,
    input DoUpdate,
    input [31:0] UpdatePC,
    input UpdateDirection
    );
   // dummy code
    reg [1:0] HTable[2047:0];

    wire [10:0] LookupIndex;
    wire [10:0] HTableIndex;
    wire [10:0] UpdateIndex;

    reg [1:0] currentState;

    assign HTableIndex = PC[12:2];
    assign UpdateIndex = UpdatePC[12:2];
    assign LookupIndex = PC[12:2];
    assign Prediction = HTable[HTableIndex][1];

    wire [1:0] initalUpdateValue;
    assign initalUpdateValue = HTable[UpdateIndex];

    assign Prediction = HTable[LookupIndex][1];

    always@(posedge clk)
    begin
    if(DoUpdate)
    begin
        if (UpdateDirection)
        begin
        if(2'b11==initialUpdateValue)
        begin
            HTable[UpdateIndex] <= 2'b11;
        end
        else
        begin
            HTable[UpdateIndex] <= initialUpdateValue + 1;
        end 
        end
        else
        begin
        if(2'b00 == initialUpdateValue)
        begin
            HTable[UpdateIndex] <= 2'b00;
        end
        else
        begin  
            HTable[UpdateIndex] <= initialUpdateValue - 1;
        end
        end
    end
    end
    
    integer i;
    initial
    begin
        for(i=0;i<2048;i=i+1) HTable[i] <= 2'b10;
    end   
          
endmodule
