package kotlin_app

import kotlin.test.Test
import kotlin.test.assertNotEquals
import kotlin.test.assertEquals

    class TriangleTest() {
    @Test
    fun checkTriangleValidityTest() {
        val classTest = Triangle()
        assertEquals("Not Valid", classTest.checkTriangleValidity(8, 100, 26))
        assertEquals("Valid", classTest.checkTriangleValidity(133, 57, 107))
    }
}