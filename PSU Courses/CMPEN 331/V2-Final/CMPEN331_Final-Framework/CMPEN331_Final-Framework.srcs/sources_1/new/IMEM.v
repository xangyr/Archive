`timescale 1ns / 1ps

module ICACHE(
    input [31:0] Address,
    input clk,
    output reg [31:0] InstBits,
    output Ready,
    output IFill, // Whether it wants stuff from memory
    output [31:0] IFill_Address, // Where it is in memory
    input [511:0] Fill_Contents
    );
    
    // 2KB Direct mapped, block size 64 byte
    // 2^11 bytes / 2^6 bytes = 2^5 sets
    // Block = 64 bytes ==> Block offset = 6 bits [5:0]
    // Set index lg2(#sets) ==> 5 bits Address [10:6]
    // Tag size = Address size - block bits - index bits = 32 - 6 - 5 ==>Address[31:11]
    
    wire [5:0] BlockOffset;
    assign BlockOffset = Address[5:0];
    wire [4:0] SetIndex;
    assign SetIndex = Address[10:6];
    wire[20:0] CurrentTag;
    assign CurrentTag = Address[31:11];
    
    wire ICacheHit;
    
    wire TagMatch;
    wire IsValid;
    wire [20:0] CheckedTag;
    wire [511:0] SelectedBlockContents;
    
    reg [0:0] Valid [31:0]; // Valid bits for eacb cache block
    reg [20:0] Tag [31:0]; // Tag for each cache block
    reg [511:0] Frames [31:0]; // Actual cache contents
    
    assign IsValid = Valid[SetIndex];
    assign CheckedTag = Tag[SetIndex];
    assign SelectedBlockContents = Frames[SetIndex];
    
    assign TagMatch = CurrentTag == CheckedTag;
    
    assign ICacheHit = IsValid & TagMatch;
    
    assign IFill = ~ICacheHit; // If we don't have the data, ask someone who does
    assign Ready = ICacheHit; // If we have the data, we are ready!
    
    assign IFill_Address = (IFill)?Address:32'h0000_0000; // Fine
    
    wire [15:0] ADDR16;
    assign ADDR16 = Address[15:0];
        
    //Should get bits from cache, and only if tag match and valid
    always @ (*)
    begin
    case (ADDR16[5:2])
    4'b0000: InstBits = SelectedBlockContents[511:480];
    4'b0001: InstBits = SelectedBlockContents[479:448];
    4'b0010: InstBits = SelectedBlockContents[447:416];
    4'b0011: InstBits = SelectedBlockContents[415:384];
    4'b0100: InstBits = SelectedBlockContents[383:352];
    4'b0101: InstBits = SelectedBlockContents[351:320];
    4'b0110: InstBits = SelectedBlockContents[319:288];
    4'b0111: InstBits = SelectedBlockContents[287:256];
    4'b1000: InstBits = SelectedBlockContents[255:224];
    4'b1001: InstBits = SelectedBlockContents[223:192];
    4'b1010: InstBits = SelectedBlockContents[191:160];
    4'b1011: InstBits = SelectedBlockContents[159:128];
    4'b1100: InstBits = SelectedBlockContents[127:96];
    4'b1101: InstBits = SelectedBlockContents[95:64];
    4'b1110: InstBits = SelectedBlockContents[63:32];
    4'b1111: InstBits = SelectedBlockContents[31:0];
    endcase
    end
    
    always @ (posedge clk)
    begin
    // write the fill data into the cache if filling. Also update metadata
    if(~ICacheHit)
    begin
        Valid[SetIndex]=1'b1;
        Tag[SetIndex]= CurrentTag;
        Frames[SetIndex]= Fill_Contents;
    end
    end

integer i;    
initial
begin
// set all cache blocks to invalid
for (i=0; i<32; i=i+1) Valid[i]=1'b0;
end    

endmodule