package com.example.android_ta

import kotlin.test.Test
import kotlin.test.assertNotEquals
import kotlin.test.assertEquals

    class TriangleTest() {
    @Test
    fun checkTriangleValidityTest() {
        val classTest = Triangle()
        assertEquals("Not Valid", classTest.checkTriangleValidity(50, -90, -106))
        assertEquals("Not Valid", classTest.checkTriangleValidity(19, -76, 151))
    }
}