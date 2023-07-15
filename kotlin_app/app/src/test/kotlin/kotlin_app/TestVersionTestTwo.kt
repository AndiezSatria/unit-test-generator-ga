package kotlin_app

import kotlin.test.Test
import kotlin.test.assertNotEquals
import kotlin.test.assertEquals

    class TestVersionTest() {
    @Test
    fun testFunctionTest() {
        assertEquals(-93, TestVersion.testFunction(-137, -44))
        assertEquals(-11424, TestVersion.testFunction(-112, 102))
        assertEquals(23, TestVersion.testFunction(29, -6))
    }
}