`timescale 1ns / 1ps

module DCACHE(
    input [31:0] Address,
    input [31:0] SValue,
    output [31:0] RValue,
    output Ready,
    input ReadMem,
    input WriteMem,
    input LBU,
    input ByteOp,
    input clk,
    output DFill,
    output [31:0] DFill_Address,
    input [255:0] Fill_Contents,
    output WriteBack,
    output [31:0] WB_Address,
    output [255:0] WB_Value    
    );
    
    // 2KB 2-way associattive, LRU, block size 32 bytes
    // 2^11 bytes / 2 ways/ 2^5 bytes - 2^5 sets
    // Block = 32 bytes ==> BO = 5 bits Address [4:0]
    //Set index lg2(#sets)==> 5 bits Address [9:5]
    // Tag size - Address size - block bits - index bits - 32 - 6 - 5 -->Address[31:10]
    
    wire [4:0] BlockOffset;
    assign BlockOffset = Address[4:0];
    wire [4:0] SetIndex;
    assign SetIndex = Address[9:5];
    wire[21:0] CurrentTag;
    assign CurrentTag = Address[31:10];
    
    wire DCacheHit;
    wire access;
    
    assign access = ReadMem | WriteMem;
    
    wire TagMatch0;
    wire IsValid0;
    wire TagMatch1;
    wire IsValid1;
    wire [21:0] CheckedTag0;
    wire [255:0] SelectedBlockContents0;
    wire [21:0] CheckedTag1;
    wire [255:0] SelectedBlockContents1;
    
    wire selectedWay;
    wire [255:0] SelectedBlockContents;
    assign SelectedBlockContents = (selectedWay)?SelectedBlockContents1:SelectedBlockContents0;
    
    reg[255:0] updateContents;
    
    reg [0:0] MRU[31:0]; // is Way 0 or is Way 1 the most recently used way for each set?
    
    //WAY 0
    reg [0:0] Valid0[31:0]; // Valid bits for each cache block
    reg [0:0] Dirty0[31:0]; // Dirty bits for each cache block
    reg[21:0] Tag0[31:0]; // Tag for each cache block
    reg[255:0] Frames0 [31:0]; // Actual cache contents
    //WAY 1
    reg [0:0] Valid1[31:0]; // Valid bits for each cache block
    reg [0:0] Dirty1[31:0]; // Dirty bits for each cache block
    reg[21:0] Tag1[31:0]; // Tag for each cache block
    reg[255:0] Frames1 [31:0]; // Actual cache contents
    
    assign IsValid0 = Valid0[SetIndex];
    assign CheckedTag0 = Tag0[SetIndex];
    assign SelectedBlockContents0 = Frames0[SetIndex];
    
    assign IsValid0 = Valid1[SetIndex];
    assign CheckedTag0 = Tag1[SetIndex];
    assign SelectedBlockContents0 = Frames1[SetIndex];
    
    
    assign TagMatch0 = CurrentTag == CheckedTag0;
    assign TagMatch1 = CurrentTag == CheckedTag1;
    
    assign selectedWay = TagMatch1 & IsValid1; // For hit, select way 1 if in way 1, else 0 (if not hit, not used)
    
    assign DCacheHit = (IsValid0 & TagMatch0) | (IsValid1 & TagMatch1); // hit if either is hit
    
    assign Ready = access & DCacheHit; // If being accessed and hit, ready, else not ready

    assign DFill = access & ~DCacheHit; // Only a miss if you were trying to access data and couldn't
    
    assign WriteBack = DFill & ((~MRU[SetIndex])?(Valid1[SetIndex]&Dirty1[SetIndex]):(Valid0[SetIndex]&Dirty0[SetIndex])); // should only be true if access caused an eviction

    assign DFill_Address = DFill?(Address):32'h0000_0000;
    
    wire [21:0] evictionTag;
    wire[255:0] evictionData;
    
    assign evictionData = (~MRU[SetIndex])?(Frames1[SetIndex]):(Frames0[SetIndex]);
    assign evictionTag = (~MRU[SetIndex])?(Tag1[SetIndex]):(Tag0[SetIndex]);
    
    assign WB_Address = WriteBack?({evictionTag,SetIndex,5'b00000}):32'h0000_0000; // FIX THIS: Should be address of block being written back, not address of current access!
    assign WB_Value = WriteBack?(evictionData):256'h0;
    
    wire [15:0] ADDR16;
    assign ADDR16=Address[15:0];
    wire [7:0] byteValue;
    assign byteValue = SValue[7:0];

    reg [31:0] mergedVal;
    reg [31:0] lwval;
    reg [31:0] lbval;
    reg [31:0] lbuval;
            
     //Should get bits from cache, and only if tag match and valid
    always @ (*)
    begin
    case (ADDR16[4:2])
    3'b000: lwval = Fill_Contents[255:224];
    3'b001: lwval = Fill_Contents[223:192];
    3'b010: lwval = Fill_Contents[191:160];
    3'b011: lwval = Fill_Contents[159:128];
    3'b100: lwval = Fill_Contents[127:96];
    3'b101: lwval = Fill_Contents[95:64];
    3'b110: lwval = Fill_Contents[63:32];
    3'b111: lwval = Fill_Contents[31:0];
    endcase
    case (ADDR16[1:0])
    2'b00: begin
    lbval = {{24{lwval[31]}},lwval[31:24]};
    lbuval = {{24{1'b0}},lwval[31:24]};
    end
    2'b01:begin
    lbval = {{24{lwval[23]}},lwval[23:16]};
    lbuval = {{24{1'b0}},lwval[23:16]};
    end
    2'b10:begin
    lbval = {{24{lwval[15]}},lwval[15:8]};
    lbuval = {{24{1'b0}},lwval[15:8]};
    end
    2'b11:begin
    lbval = {{24{lwval[7]}},lwval[7:0]};
    lbuval = {{24{1'b0}},lwval[7:0]};
    end
    endcase
    mergedVal=lwval;
    if(ByteOp)
    begin
    case (WB_Address[1:0])
    2'b00: mergedVal={byteValue,lwval[23:0]};
    2'b01: mergedVal={lwval[31:24],byteValue,lwval[15:0]};
    2'b10: mergedVal={lwval[31:16],byteValue,lwval[7:0]};
    2'b11: mergedVal={lwval[31:8],byteValue};
    endcase
    end
    else
        begin
        mergedVal=SValue;
        end
    end
    
    wire [31:0] readValue;
    assign readValue = ByteOp?(LBU?lbuval:lbval):lwval;
    assign RValue = ReadMem?readValue:32'h0000_0000;
    
    always@(posedge clk)
    begin
    // update cache contents, metadata
    if (DFill)
    begin
    MRU[SetIndex]<=~MRU[SetIndex];
    if(MRU[SetIndex])
    begin
    Valid0[SetIndex]<=1'b1;
    Dirty0[SetIndex]<=1'b1;
    Tag0[SetIndex]<=CurrentTag;
    Frames0[SetIndex]<=Fill_Contents;
    end
    else
    begin
    Valid1[SetIndex]<=1'b1;
    Dirty1[SetIndex]<=1'b1;
    Tag1[SetIndex]<=CurrentTag;
    Frames1[SetIndex]<=Fill_Contents;
    end
    end
    else
    begin
        if (DCacheHit & WriteMem)
        begin
            case (WB_Address[4:2])
            3'b000: WB_Value = {mergedVal,Fill_Contents[223:0]};
            3'b001: WB_Value = {Fill_Contents[255:224],mergedVal,Fill_Contents[191:0]};
            3'b010: WB_Value = {Fill_Contents[255:192],mergedVal,Fill_Contents[159:0]};
            3'b011: WB_Value = {Fill_Contents[255:160],mergedVal,Fill_Contents[127:0]};
            3'b100: WB_Value = {Fill_Contents[255:128],mergedVal,Fill_Contents[95:0]};
            3'b101: WB_Value = {Fill_Contents[255:96],mergedVal,Fill_Contents[63:0]};
            3'b110: WB_Value = {Fill_Contents[255:64],mergedVal,Fill_Contents[31:0]};
            3'b111: WB_Value = {Fill_Contents[255:32],mergedVal};
            endcase
            MRU[SetIndex]<=selectedWay;
            if(selectedWay)
            begin
            Dirty1[SetIndex]=1'b1;
            Frames1[SetIndex]=updateContents;
            end
            else
            begin
            Dirty0[SetIndex]=1'b1;
            Frames0[SetIndex]=updateContents;
            end
        end
    if (DCacheHit & ReadMem)
        begin
        MRU[SetIndex]<=selectedWay;
        end
        end
    end

integer i;
initial
begin
// set metadata to invalid, initialize NMRU bits
for(i=0; i<32; i=i+1)
begin
MRU[i]=1'b0;
Valid0[i]=1'b0;
Valid1[i]=1'b0;
end
end
endmodule