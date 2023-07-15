package com.example.android_ta

import kotlin.test.Test
import kotlin.test.assertNotEquals
import kotlin.test.assertEquals

    class NthFibonacciTest() {
    @Test
    fun nthFibonacciTest() {
val classTest = NthFibonacci()
        assertEquals(-1725907855, classTest.nthFibonacci(169))
    }
}