; Helper PRG bank2. Native encoded32 now selects canonical mirror bank18.
; Origin95F9 replaces helper-only data; original strings remain in canonical bank18.
; FDD3/FDDB select/restore the native 8000/A000 pair. No NMI/IRQ hook here.
; FE53..FE5C native idle loop is19cycles. Path padding aligns added time:
; page133 or152cycles; setup114cycles. Register/flags restored by bootstrap.
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
    LDY #$00
    STY $06C3
    STY $06C4
    LDA $06CE
    CMP #$95
    BNE @second
    LDA $06CD
    CMP #$F9
    BNE @second
    LDA #$80
    NOP
    NOP
    NOP
    BNE @store
second:
    LDA $06CE
    CMP #$96
    BNE @fallback
    LDA $06CD
    CMP #$15
    BNE @fallback_low
    LDA #$84
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    BNE @store
fallback_low:
    NOP
    NOP
    NOP
    NOP
    JMP @fallback
fallback:
    BIT $C6
    NOP
    NOP
    LDA #$5A
store:
    STA $C6
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
    NOP
    NOP
    NOP
    NOP
    NOP
    JMP $FDDB
