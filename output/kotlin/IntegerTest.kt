package com.example.android_ta

import kotlin.test.Test
import kotlin.test.assertNotEquals
import kotlin.test.assertEquals

class IntegerTest() {
    @Test
    fun isPrimeTest() {
        assertEquals(false,Integer.isPrime(-237))
        assertEquals(true,Integer.isPrime(199))
    }
}