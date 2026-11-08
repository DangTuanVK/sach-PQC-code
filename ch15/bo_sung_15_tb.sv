// Không có trong sách: testbench cho khối cánh bướm (Mã nguồn 15.1). Tái tạo kết quả in sau Mã nguồn 15.1 (chapters/ch16/main.tex).
// Day 2000 bo ba (a, b, zeta) ngau nhien vao khoi canh buom, luu gia tri ky vong vao hang doi
// de bu do tre ba chu ky, sau do so tung ket qua voi mo hinh tham chieu mont_ref (Ma nguon 16.1b).
`timescale 1ns/1ns
module tb;
    localparam longint Q = 3329;
    localparam int     SO_BO = 2000;

    // mo hinh tham chieu cua sach (Ma nguon 16.1b), dung nguyen van
    `include "MONT_REF_FILE"

    logic clk = 0, rst_n = 0, vld_i = 0;
    logic signed [15:0] a_i = 0, b_i = 0, zeta_i = 0;
    logic vld_o;
    logic signed [15:0] a_o, b_o;

    butterfly dut (.*);

    always #5 clk = ~clk;

    typedef struct { int a_kv, b_kv; } ky_vong_t;
    ky_vong_t hang_doi[$];
    int da_day = 0, da_so = 0, khop = 0;

    function automatic int ngau_nhien_tam();    // he so trong (-q/2, q/2]
        return int'($urandom_range(Q - 1)) - int'((Q - 1) / 2);
    endfunction

    initial begin
        void'($urandom(2026));                  // hat giong co dinh
        repeat (5) @(posedge clk);
        rst_n <= 1;
        @(posedge clk);
        while (da_day < SO_BO) begin            // moi chu ky day mot bo ba
            int a, b, z, t;
            ky_vong_t kv;
            a = ngau_nhien_tam(); b = ngau_nhien_tam(); z = ngau_nhien_tam();
            t = mont_ref(longint'(z) * longint'(b));
            kv.a_kv = a + t; kv.b_kv = a - t;
            hang_doi.push_back(kv);
            a_i <= a; b_i <= b; zeta_i <= z; vld_i <= 1;
            da_day++;
            @(posedge clk);
        end
        vld_i <= 0;
    end

    always @(posedge clk) begin                 // so ket qua khi vld_o bat
        if (rst_n && vld_o) begin
            ky_vong_t kv;
            kv = hang_doi.pop_front();
            da_so++;
            if (a_o == kv.a_kv && b_o == kv.b_kv) khop++;
            else $display("LECH tai bo %0d: (%0d, %0d) != (%0d, %0d)",
                          da_so, a_o, b_o, kv.a_kv, kv.b_kv);
            if (da_so == SO_BO) begin
                $display("KET QUA: %0d/%0d truong hop khop mo hinh tham chieu", khop, SO_BO);
                if (khop == SO_BO) $display("BUTTERFLY OK");
                $finish;
            end
        end
    end
endmodule
