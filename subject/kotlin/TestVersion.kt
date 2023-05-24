package kotlin_app

/**
 * Created by AndiezSatria on 22/05/2023.
 */
class TestVersion {
    companion object {
        fun testFunction(x: Int, y: Int): Int {
            return if (x > 0) x + y
            else if (y > 0) x * y
            else x - y
        }
    }
}