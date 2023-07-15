package kotlin_app

/**
 * Created by AndiezSatria on 28/05/2023.
 */
object Integer {
    fun isPrime(n: Int): Boolean {
        if (n <= 1) return false
        if (n == 2 || n == 3) return true
        if (n % 2 == 0 || n % 3 == 0) return false
        var i = 5
        while (i <= Math.sqrt(n.toDouble())) {
            if (n % i == 0 || n % (i + 2) == 0) return false
            i += 6
        }
        return true
    }
}