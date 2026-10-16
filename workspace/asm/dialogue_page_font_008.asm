;008: odd custom font-bank pairs supply native top RAM34 as well as06F3.
; All original/intro/home/default banks are even. Gate Japanese clone171 is odd.
;11-cycle dispatch on both paths; use stored pointer high07 for one-cycle saving;
;remove10cycles from both native delay paths. No source code cave or new scratch RAM.
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
    LSR A
    BCC @no_top
    ROL A
    STA $34
    NOP
    LDY #$00
    STY $06C3
    STY $06C4
    LDA $07
    CMP #$96
    BNE @short_top
    BIT $C6
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    JMP @restore_top
short_top:
restore_top:
    JMP $FDDB
no_top:
    ROL A
    NOP
    NOP
    LDY #$00
    STY $06C3
    STY $06C4
    LDA $07
    CMP #$96
    BNE @short_plain
    BIT $C6
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    JMP @restore_plain
short_plain:
restore_plain:
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
