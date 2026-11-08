// Mã nguồn 16.1 - Khối cánh bướm Cooley-Tukey với rút gọn Montgomery, viết bằng SystemVerilog. Ba tầng đường ống tách phép nhân, phép rút gọn và phép cộng/trừ.
// Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 16, trang 325
// Trích tự động từ chapters/ch16/main.tex (dòng 208) bằng extract.py; không sửa tay file này.

module butterfly #(
    parameter logic signed [15:0] Q    = 16'sd3329,
    parameter logic        [15:0] QINV = 16'd62209   // q^{-1} mod 2^16
)(
    input  logic               clk, rst_n, vld_i,
    input  logic signed [15:0] a_i, b_i, zeta_i,
    output logic               vld_o,
    output logic signed [15:0] a_o, b_o
);
    logic signed [31:0] prod_q1;
    logic signed [15:0] a_q1, t_q2, a_q2;   logic vld_q1, vld_q2;

    // rut gon Montgomery: tra ve x * R^{-1} mod q, R = 2^16
    function automatic logic signed [15:0]
             mont_reduce(input logic signed [31:0] x);
        logic        [15:0] m;
        logic signed [31:0] t;
        m = x[15:0] * QINV;              // tinh mod 2^16, TRAN LA CO Y
        t = x - $signed({1'b0, m}) * Q;
        return t[31:16];                 // chia 2^16 bang cach lay bit cao
    endfunction

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin vld_q1 <= 0; vld_q2 <= 0; vld_o <= 0; end
        else begin
            prod_q1 <= zeta_i * b_i;           // tang 1: nhan 16x16 -> 32 bit
            a_q1    <= a_i;
            vld_q1  <= vld_i;
            t_q2    <= mont_reduce(prod_q1);   // tang 2: rut gon
            a_q2    <= a_q1;
            vld_q2  <= vld_q1;
            a_o     <= a_q2 + t_q2;            // tang 3: cong va tru
            b_o     <= a_q2 - t_q2;
            vld_o   <= vld_q2;
        end
    end
endmodule
