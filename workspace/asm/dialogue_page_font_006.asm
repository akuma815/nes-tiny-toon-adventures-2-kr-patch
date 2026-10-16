; Defers active font when native06DF=4 pre-clear init; commits on repeated06DF=3 init after5-row clear.
; Actual06F3 font bank; native home IRQ keeps all status reads and instruction boundaries.
; Fourth page helper, source pointer table consumed before slot font lookup.
; Helper-only font table9700..97FF: all48 native slots and default padding.
; All valid slots add19 cycles to008/020, retaining19-cycle idle-loop phase; actual timing required.
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
    LDA $06DF
    CMP #$04
    BEQ @defer
    LDA $C6
    STA $06F3
    JMP @joined
defer:
    BIT $C6
    NOP
    NOP
    NOP
joined:
    BIT $C6
    NOP
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
    NOP
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
    STA $06F3
    NOP
    NOP
    NOP
    JMP $FDDB
