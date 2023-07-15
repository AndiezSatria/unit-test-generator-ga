package com.example.android_ta

import kotlin.test.Test
import kotlin.test.assertNotEquals
import kotlin.test.assertEquals

    class TestVersionTest() {
    @Test
    fun testFunctionTest() {
        assertEquals(-5, TestVersion.testFunction(-107, -102))
        assertEquals(62, TestVersion.testFunction(44, 18))
        assertEquals(-352, TestVersion.testFunction(-8, 44))
    }
}