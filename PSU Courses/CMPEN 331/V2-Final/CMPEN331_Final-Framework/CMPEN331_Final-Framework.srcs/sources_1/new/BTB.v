module BTB(
input clk,
input [31:0] accessPC,
output [31:0] outInstBits,
output [31:0] targetPC,
output btbHit,
output btbType,
input update_ctrl,
input [31:0] updatePC,
input [31:0] updateInstBits,
input [31:0] updateTargetPC
);

// 1 entry per entry Block offest = lg2(1) = 0 bits
// 32 entry in mem - set index lg2(32) = 5 bits
// 32 - 5 = 27

reg [0:0] IsValid [31:0];
reg [26:0] BTBTag [31:0];
reg [31:0] InstContents[31:0];
reg [31:0] InstAddress [31:0];
reg [0:0] IsJump [31:0];

wire [4:0] Index;
wire [26:0] IncomingTag;

wire [4:0] UpdateIndex;
wire [26:0] UpdateLookupTag;

wire CurrentValid;
wire [26:0] LookupTag;
wire [31:0] CurrentContents;
wire [31:0] CurrentAddress;
wire LookupIsJump;

// low two bits of PC always zero
assign Index = accessPC[6:2];
assign IncomingTag = accessPC[31:5];

assign UpdateIndex = updatePC[6:2];
assign UpdateLookupTag = updatePC[31:5];

assign CurrentValid = IsValid[Index];
assign LookupTag = BTBTag[Index];
assign CurrentContents = InstContents[Index];
assign CurrentAddress = InstAddress[Index];
assign LookupIsJump = IsJump[Index];

assign btbHit = (CurrentValid & (LookupTag == IncomingTag));
assign outInstBits = CurrentContents;
assign LargeLPC = CurrentAddress;
assign btbType = LookupIsJump;
//YOUR CODE HERE
always @(posedge clk)
begin 
if (update_ctrl)
begin
    IsValid[UpdateIndex] <= 1'b1;
    BTBTag[UpdateIndex] <= UpdateLookupTag;
    InstContents[UpdateIndex] <= updateInstBits;
    InstAddress[UpdateIndex] <= updateTargetPC;
    IsJump[UpdateIndex] <= (updateInstBits[31:26] == 6'b000010) | (updateInstBits[31:26] == 6'b000011);
end 
end

integer i;
initial
begin
for (i=0; i<32; i=i+1) IsValid [i] <= 1'b0;
end
endmodule