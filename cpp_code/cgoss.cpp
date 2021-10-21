#include <pybind11/pybind11.h>
namespace py = pybind11;


float maxd2(float a, float b){
    float a2;
    float b2;
    float c = 0.5;
    float scale = 1.0;
    if (a < c) 
        a2 = std::abs((scale - a) - c);
    else
        a2 =a - c;
    if (b < c) 
        b2 = std::abs((scale - b) - c);
    else
        b2 = b - c;
    
    if (b2 > a2){
        return b;
    }
    
    return a;
    


}
float maxd3(float a, float b, float c){
    float a2;
    float b2;
    float scale = c * 2;
    if (a < c) 
        a2 = std::abs((scale - a) - c);
    else
        a2 =a - c;
    if (b < c) 
        b2 = std::abs((scale - b) - c);
    else
        b2 = b - c;
    
    if (b2 > a2){
        return b;
    }
    
    return a;
    


}


float scale_confidence(float a, float b){
    float c = 0.5;
    if (a < c) 
        a += (a*b);
    else
        a -= (a*b);
    return a;
}



PYBIND11_MODULE(cgoss, m) {
    m.doc() = "pybind11 helper functions"; // optional module docstring

    m.def("max_distance", &maxd2, "A function which return one of two floats based on its distance from 0.5. Floats must be between 0-1");
    m.def("max_distance", &maxd3, "A function which return one of two floats based on its distance from a third. Floats must be between 0-c*2");
    m.def("scale_confidence", &scale_confidence, "Reduces the confidence of a prediction by a percentage of the prediction.");
}