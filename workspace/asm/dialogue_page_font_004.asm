; Encoded06F3 latch for distinct home IRQ; default0 decodes native90.
; Source clear FE40/CFB4 before UI; observed active UI ownership gate.
; Fourth page helper, source pointer table consumed before slot font lookup.
; Helper-only font table9700..97FF: all48 native slots and default padding.
; All valid slots retain EXACT adopted008/012 elapsed cycles, not only mod19.
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
    EOR #$5A
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
    JMP @restore
short:
    NOP
    NOP
    NOP
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
    EOR #$5A
    STA $06F3
    NOP
    NOP
    JMP $FDDB
