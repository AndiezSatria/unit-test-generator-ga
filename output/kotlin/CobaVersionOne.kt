package com.example.android_ta

class CobaTest() {
    @Test
    fun isOddTest() {
        assertEquals(Coba.isOdd(8897, "v8:*6=\"~"), False)
        assertEquals(Coba.isOdd(2007, "<#"), False)
        assertEquals(Coba.isOdd(5736, "v:}4c+[-idS"), False)
    }
    @Test
    fun stringProgramTest() {
        assertEquals(Coba.stringProgram("/3-+"), 4162)
        assertEquals(Coba.stringProgram("9[\gdiuo/tD@6+-"), 7965)
        assertEquals(Coba.stringProgram("!PXE&u]])+C_L"), 8978)
        assertEquals(Coba.stringProgram("wh\[mOB"), 7332)
        assertEquals(Coba.stringProgram("D@*@S2pfa=B.k,9bVeTO"), 4069)
    }
}