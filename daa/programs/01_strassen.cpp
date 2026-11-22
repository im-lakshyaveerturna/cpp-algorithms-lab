// Experiment 1: Strassen's matrix multiplication (divide and conquer).
#include <iostream>
#include <vector>

using Matrix = std::vector<std::vector<long long>>;

// Return A + sign * B, where sign is +1 or -1.
Matrix combine(const Matrix& a, const Matrix& b, int sign = 1) {
    Matrix result = a;
    for (std::size_t i = 0; i < a.size(); ++i)
        for (std::size_t j = 0; j < a.size(); ++j)
            result[i][j] += sign * b[i][j];
    return result;
}

Matrix strassen(const Matrix& a, const Matrix& b) {
    const std::size_t n = a.size();
    if (n == 1) return {{a[0][0] * b[0][0]}};

    const std::size_t h = n / 2;
    Matrix a11(h, std::vector<long long>(h)), a12 = a11, a21 = a11, a22 = a11;
    Matrix b11 = a11, b12 = a11, b21 = a11, b22 = a11;
    for (std::size_t i = 0; i < h; ++i) {
        for (std::size_t j = 0; j < h; ++j) {
            a11[i][j] = a[i][j];         a12[i][j] = a[i][j + h];
            a21[i][j] = a[i + h][j];     a22[i][j] = a[i + h][j + h];
            b11[i][j] = b[i][j];         b12[i][j] = b[i][j + h];
            b21[i][j] = b[i + h][j];     b22[i][j] = b[i + h][j + h];
        }
    }

    // Seven recursive multiplications instead of the usual eight.
    const Matrix m1 = strassen(combine(a11, a22), combine(b11, b22));
    const Matrix m2 = strassen(combine(a21, a22), b11);
    const Matrix m3 = strassen(a11, combine(b12, b22, -1));
    const Matrix m4 = strassen(a22, combine(b21, b11, -1));
    const Matrix m5 = strassen(combine(a11, a12), b22);
    const Matrix m6 = strassen(combine(a21, a11, -1), combine(b11, b12));
    const Matrix m7 = strassen(combine(a12, a22, -1), combine(b21, b22));

    const Matrix c11 = combine(combine(combine(m1, m4), m5, -1), m7);
    const Matrix c12 = combine(m3, m5);
    const Matrix c21 = combine(m2, m4);
    const Matrix c22 = combine(combine(combine(m1, m2, -1), m3), m6);
    Matrix c(n, std::vector<long long>(n));
    for (std::size_t i = 0; i < h; ++i) {
        for (std::size_t j = 0; j < h; ++j) {
            c[i][j] = c11[i][j];         c[i][j + h] = c12[i][j];
            c[i + h][j] = c21[i][j];     c[i + h][j + h] = c22[i][j];
        }
    }
    return c;
}

int main() {
    int n;
    if (!(std::cin >> n) || n < 1 || n > 128) {
        std::cerr << "Error: matrix order must be between 1 and 128.\n";
        return 1;
    }
    int padded = 1;
    while (padded < n) padded *= 2;
    Matrix a(padded, std::vector<long long>(padded)), b = a;
    for (Matrix* matrix : {&a, &b}) {
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                if (!(std::cin >> (*matrix)[i][j]) || (*matrix)[i][j] < -10000 ||
                    (*matrix)[i][j] > 10000) {
                    std::cerr << "Error: supply two matrices with integer entries in [-10000, 10000].\n";
                    return 1;
                }
            }
        }
    }
    // Zero padding handles orders that are not powers of two.
    const Matrix c = strassen(a, b);
    std::cout << "Product matrix:\n";
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j)
            std::cout << (j == 0 ? "" : " ") << c[i][j];
        std::cout << '\n';
    }
}
