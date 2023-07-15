package kotlin_app

/**
 * Created by AndiezSatria on 28/05/2023.
 */
class Triangle {
    fun checkTriangleValidity(a: Int, b: Int, c:Int): String {
        return if (a + b <= c || a + c <= b || b + c <= a)
            "Not Valid"
        else
            "Valid"
    }
}