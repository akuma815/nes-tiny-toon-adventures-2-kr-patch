; Actual06F3 font bank; native home IRQ keeps all status reads and instruction boundaries.
; Fourth page helper, source pointer table consumed before slot font lookup.
; Helper-only font table9700..97FF: all48 native slots and default padding.
; Non-gate short path consumes same10 cycles as005. Gate native06D0=12 commits RAM34 with19 extra cycles; actual IRQ/NMI regression required.
page_init:
    LDA $06CF
    ASL A
    TAY
    LDA $9599,Y
    STA $06CD
    STA $06
    LDA $959A,Y
    STA $06CE
    STA $07
    LDA $9700,Y
    STA $C6
    STA $06F3
    LDY #$00
    STY $06C3
    STY $06C4
    LDA $06CE
    CMP #$96
    BNE @short
    BIT $C6
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    JMP @restore
short:
    LDA $06D0
    CMP #$12
    BEQ @gate_commit
    NOP
restore:
    JMP $FDDB
intro_setup:
    LDA #$00
    JSR $8E16
    JSR $8E1D
    JSR $8E00
    STA $0618
    STA $06C3
    STA $040F
    LDA #$01
    STA $06CF
    LDA #$80
    STA $C6
    STA $06F3
    NOP
    NOP
    NOP
    JMP $FDDB

gate_commit:
    LDA $06F3
    STA $34
    BIT $C6
    NOP
    NOP
    NOP
    NOP
    NOP
    JMP $FDDB
