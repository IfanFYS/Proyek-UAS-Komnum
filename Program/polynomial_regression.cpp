#include <iostream>
#include <vector>
#include <fstream>
#include <iomanip>
#include <cmath>
#include <string> // Required for std::string, std::to_string

// Structure to hold data points
struct DataPoint {
    double x;
    double y;
};

// Function to get the directory part of a path
std::string getExecutableDir(const std::string& executable_path) {
    size_t last_slash_idx = executable_path.rfind('/');
    if (std::string::npos == last_slash_idx) {
        last_slash_idx = executable_path.rfind('\\'); // For Windows paths
    }
    if (std::string::npos != last_slash_idx) {
        return executable_path.substr(0, last_slash_idx + 1); // Include the trailing slash
    }
    return ""; // No path separator, assume CWD or it's just the exe name
}


// Function to read data from a file given its full path
std::vector<DataPoint> readDataFromFullPath(const std::string& full_path_to_data) {
    std::vector<DataPoint> data;
    std::cout << "Attempting to read data from full path: " << full_path_to_data << std::endl;
    std::ifstream file(full_path_to_data);
    if (!file.is_open()) {
        std::cerr << "Error: Could not open data file " << full_path_to_data << std::endl;
        return data;
    }
    DataPoint p;
    while (file >> p.x >> p.y) {
        data.push_back(p);
    }
    file.close();
    if (!data.empty()) {
        std::cout << "Successfully read data from: " << full_path_to_data << std::endl;
    }
    return data;
}

// Function to print a matrix (for debugging)
void printMatrix(const std::vector<std::vector<double>>& matrix) {
    for (const auto& row : matrix) {
        for (double val : row) {
            std::cout << std::setw(10) << val << " ";
        }
        std::cout << std::endl;
    }
}

// Function to print a vector (for debugging)
void printVector(const std::vector<double>& vec) {
    for (double val : vec) {
        std::cout << std::setw(10) << val << " ";
    }
    std::cout << std::endl;
}

// Function to perform Gaussian elimination to solve Ax = B
std::vector<double> gaussianElimination(std::vector<std::vector<double>> A, std::vector<double> B) {
    int n = B.size();
    for (int i = 0; i < n; ++i) {
        int maxRow = i;
        for (int k = i + 1; k < n; ++k) {
            if (std::abs(A[k][i]) > std::abs(A[maxRow][i])) {
                maxRow = k;
            }
        }
        std::swap(A[i], A[maxRow]);
        std::swap(B[i], B[maxRow]);
        double pivot = A[i][i];
        if (std::abs(pivot) < 1e-9) {
             std::cerr << "Error: Matrix is singular or nearly singular." << std::endl;
             return {};
        }
        for (int j = i; j < n; ++j) A[i][j] /= pivot;
        B[i] /= pivot;
        for (int k = 0; k < n; ++k) {
            if (k != i) {
                double factor = A[k][i];
                for (int j = i; j < n; ++j) A[k][j] -= factor * A[i][j];
                B[k] -= factor * B[i];
            }
        }
    }
    return B;
}

// Function to perform polynomial regression
std::vector<double> polynomialRegression(const std::vector<DataPoint>& data, int degree) {
    int n_points = data.size();
    int m_coeffs = degree + 1;

    if (n_points == 0) { std::cerr << "Error: No data points." << std::endl; return {}; }
    if (degree < 0) { std::cerr << "Error: Degree must be non-negative." << std::endl; return {}; }
    if (n_points < m_coeffs) { std::cerr << "Error: Not enough data points for degree " << degree << std::endl; return {}; }

    std::vector<std::vector<double>> SumX(m_coeffs, std::vector<double>(m_coeffs, 0.0));
    std::vector<double> SumXY(m_coeffs, 0.0);
    std::vector<double> x_powers_sum(2 * degree + 1, 0.0);

    for (const auto& p : data) {
        for (int j = 0; j <= 2 * degree; ++j) {
            x_powers_sum[j] += std::pow(p.x, j);
        }
    }
    for (int i = 0; i < m_coeffs; ++i) {
        for (int j = 0; j < m_coeffs; ++j) {
            SumX[i][j] = x_powers_sum[i + j];
        }
    }
    for (const auto& p : data) {
        for (int i = 0; i < m_coeffs; ++i) {
            SumXY[i] += p.y * std::pow(p.x, i);
        }
    }

    std::cout << "Normal Equations Matrix (SumX) for degree " << degree << ":" << std::endl;
    printMatrix(SumX);
    std::cout << "Normal Equations Vector (SumXY) for degree " << degree << ":" << std::endl;
    printVector(SumXY);

    return gaussianElimination(SumX, SumXY);
}

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cerr << "Usage: " << (argc > 0 ? argv[0] : "polynomial_regression") 
                  << " <polynomial_degree> <full_path_to_data_file>" << std::endl;
        std::cerr << "Example: ./polyreg.exe 2 \"C:/path/to/data.txt\"" << std::endl;
        return 1;
    }

    int polynomialDegree = 2; 
    std::string dataFileFullPath = "";
    std::string executableDir = "";

    if (argc > 0 && argv[0] != nullptr) {
        executableDir = getExecutableDir(argv[0]);
    }
     std::cout << "Executable directory determined as: " << executableDir << std::endl;


    try {
        polynomialDegree = std::stoi(argv[1]);
        if (polynomialDegree < 0) {
            std::cerr << "Error: Polynomial degree must be non-negative. Got: " << argv[1] << std::endl;
            return 1;
        }
    } catch (const std::invalid_argument& ia) {
        std::cerr << "Invalid argument for polynomial degree: " << argv[1] << std::endl;
        return 1;
    } catch (const std::out_of_range& oor) {
        std::cerr << "Argument for polynomial degree out of range: " << argv[1] << std::endl;
        return 1;
    }

    dataFileFullPath = argv[2];
    std::cout << "Using Polynomial Degree: " << polynomialDegree << std::endl;
    std::cout << "Data file path: " << dataFileFullPath << std::endl;

    std::vector<DataPoint> data = readDataFromFullPath(dataFileFullPath);

    if (data.empty()) {
        std::cerr << "Exiting due to data loading error." << std::endl;
        return 1;
    }

    std::cout << "Data points read: " << data.size() << std::endl;

    std::vector<double> coefficients = polynomialRegression(data, polynomialDegree);

    if (!coefficients.empty()) {
        std::cout << "\nCalculated Polynomial Coefficients (a0, ..., an) for degree " << polynomialDegree << ":" << std::endl;
        for (size_t i = 0; i < coefficients.size(); ++i) {
            std::cout << "a" << i << ": " << coefficients[i] << std::endl;
        }

        std::string coeffFilenameBase = "coefficients_deg" + std::to_string(polynomialDegree) + ".txt";
        std::string coeffFileFullPath = executableDir + coeffFilenameBase; // Save in executable's directory

        std::ofstream coeffFile(coeffFileFullPath);
        if (coeffFile.is_open()) {
            for (double coeff : coefficients) {
                coeffFile << coeff << std::endl;
            }
            coeffFile.close();
            std::cout << "\nCoefficients saved to " << coeffFileFullPath << std::endl;
        } else {
            std::cerr << "Error: Could not open " << coeffFileFullPath << " for writing." << std::endl;
            // Fallback to CWD if writing to exe dir fails (e.g. permissions)
            std::cerr << "Attempting to save to CWD: " << coeffFilenameBase << std::endl;
            std::ofstream coeffFileCWD(coeffFilenameBase);
            if (coeffFileCWD.is_open()) {
                 for (double coeff : coefficients) {
                    coeffFileCWD << coeff << std::endl;
                }
                coeffFileCWD.close();
                std::cout << "\nCoefficients saved to " << coeffFilenameBase << " (in CWD as fallback)" << std::endl;
            } else {
                std::cerr << "Error: Could not open " << coeffFilenameBase << " for writing in CWD either." << std::endl;
            }
        }
    } else {
        std::cerr << "Polynomial regression failed for degree " << polynomialDegree << "." << std::endl;
        return 1;
    }

    return 0;
}

/*
Example of data.txt (to be provided via full path):
0.0 1.1
0.5 1.8
1.0 2.7
1.5 4.5
2.0 5.8
2.5 8.0
3.0 10.1
3.5 13.5
4.0 17.3
4.5 21.0
5.0 25.5
5.5 30.0
6.0 36.2
*/
