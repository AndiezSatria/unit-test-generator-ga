package kotlin_app

/**
 * Created by AndiezSatria on 27/05/2023.
 */
class NthFibonacci {
    fun nthFibonacci(n: Int): Int {
        var a = 0
        var b = 1
        var c: Int
        if (n == 0) return a
        for (i in 2..n) {
            c = a + b
            a = b
            b = c
        }
        return b
    }
}