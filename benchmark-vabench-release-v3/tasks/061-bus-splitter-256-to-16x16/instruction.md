# Bus Splitter 256 To 16x16

Implement one Verilog-A DUT file named `bus_split_256_to_16x16.va`.

## Interface

Define module `bus_split_256_to_16x16` with scalar electrical ports in this exact order:

```text
in255, in254, in253, in252, in251, in250, in249, in248, in247, in246, in245, in244, in243, in242, in241, in240, in239, in238, in237, in236, in235, in234, in233, in232, in231, in230, in229, in228, in227, in226, in225, in224, in223, in222, in221, in220, in219, in218, in217, in216, in215, in214, in213, in212, in211, in210, in209, in208, in207, in206, in205, in204, in203, in202, in201, in200, in199, in198, in197, in196, in195, in194, in193, in192, in191, in190, in189, in188, in187, in186, in185, in184, in183, in182, in181, in180, in179, in178, in177, in176, in175, in174, in173, in172, in171, in170, in169, in168, in167, in166, in165, in164, in163, in162, in161, in160, in159, in158, in157, in156, in155, in154, in153, in152, in151, in150, in149, in148, in147, in146, in145, in144, in143, in142, in141, in140, in139, in138, in137, in136, in135, in134, in133, in132, in131, in130, in129, in128, in127, in126, in125, in124, in123, in122, in121, in120, in119, in118, in117, in116, in115, in114, in113, in112, in111, in110, in109, in108, in107, in106, in105, in104, in103, in102, in101, in100, in99, in98, in97, in96, in95, in94, in93, in92, in91, in90, in89, in88, in87, in86, in85, in84, in83, in82, in81, in80, in79, in78, in77, in76, in75, in74, in73, in72, in71, in70, in69, in68, in67, in66, in65, in64, in63, in62, in61, in60, in59, in58, in57, in56, in55, in54, in53, in52, in51, in50, in49, in48, in47, in46, in45, in44, in43, in42, in41, in40, in39, in38, in37, in36, in35, in34, in33, in32, in31, in30, in29, in28, in27, in26, in25, in24, in23, in22, in21, in20, in19, in18, in17, in16, in15, in14, in13, in12, in11, in10, in9, in8, in7, in6, in5, in4, in3, in2, in1, in0, out15_15, out15_14, out15_13, out15_12, out15_11, out15_10, out15_9, out15_8, out15_7, out15_6, out15_5, out15_4, out15_3, out15_2, out15_1, out15_0, out14_15, out14_14, out14_13, out14_12, out14_11, out14_10, out14_9, out14_8, out14_7, out14_6, out14_5, out14_4, out14_3, out14_2, out14_1, out14_0, out13_15, out13_14, out13_13, out13_12, out13_11, out13_10, out13_9, out13_8, out13_7, out13_6, out13_5, out13_4, out13_3, out13_2, out13_1, out13_0, out12_15, out12_14, out12_13, out12_12, out12_11, out12_10, out12_9, out12_8, out12_7, out12_6, out12_5, out12_4, out12_3, out12_2, out12_1, out12_0, out11_15, out11_14, out11_13, out11_12, out11_11, out11_10, out11_9, out11_8, out11_7, out11_6, out11_5, out11_4, out11_3, out11_2, out11_1, out11_0, out10_15, out10_14, out10_13, out10_12, out10_11, out10_10, out10_9, out10_8, out10_7, out10_6, out10_5, out10_4, out10_3, out10_2, out10_1, out10_0, out9_15, out9_14, out9_13, out9_12, out9_11, out9_10, out9_9, out9_8, out9_7, out9_6, out9_5, out9_4, out9_3, out9_2, out9_1, out9_0, out8_15, out8_14, out8_13, out8_12, out8_11, out8_10, out8_9, out8_8, out8_7, out8_6, out8_5, out8_4, out8_3, out8_2, out8_1, out8_0, out7_15, out7_14, out7_13, out7_12, out7_11, out7_10, out7_9, out7_8, out7_7, out7_6, out7_5, out7_4, out7_3, out7_2, out7_1, out7_0, out6_15, out6_14, out6_13, out6_12, out6_11, out6_10, out6_9, out6_8, out6_7, out6_6, out6_5, out6_4, out6_3, out6_2, out6_1, out6_0, out5_15, out5_14, out5_13, out5_12, out5_11, out5_10, out5_9, out5_8, out5_7, out5_6, out5_5, out5_4, out5_3, out5_2, out5_1, out5_0, out4_15, out4_14, out4_13, out4_12, out4_11, out4_10, out4_9, out4_8, out4_7, out4_6, out4_5, out4_4, out4_3, out4_2, out4_1, out4_0, out3_15, out3_14, out3_13, out3_12, out3_11, out3_10, out3_9, out3_8, out3_7, out3_6, out3_5, out3_4, out3_3, out3_2, out3_1, out3_0, out2_15, out2_14, out2_13, out2_12, out2_11, out2_10, out2_9, out2_8, out2_7, out2_6, out2_5, out2_4, out2_3, out2_2, out2_1, out2_0, out1_15, out1_14, out1_13, out1_12, out1_11, out1_10, out1_9, out1_8, out1_7, out1_6, out1_5, out1_4, out1_3, out1_2, out1_1, out1_0, out0_15, out0_14, out0_13, out0_12, out0_11, out0_10, out0_9, out0_8, out0_7, out0_6, out0_5, out0_4, out0_3, out0_2, out0_1, out0_0
```

Use `vdd=0.9`, `vth=0.45`, and `tr=20p` unless compatible parameters are needed. Treat logic inputs as 0/0.9 V using `vth`.

## Required Behavior

Map bit `N` to block `N/16` and bit `N%16` without inversion or reordering.

Drive high outputs near `vdd` and low outputs near 0 V using smooth Verilog-A contributions.

## Output

Return exactly `bus_split_256_to_16x16.va`. Do not generate a Spectre testbench.
