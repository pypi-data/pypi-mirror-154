#define PY_SSIZE_T_CLEAN
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <numpy/arrayobject.h>

double d_1, d_2, c1, c2, c3;
int n, m, v, m_min;
int N, M;

#define GET3(arr, i, j, k) *((double *)PyArray_GETPTR3(arr, i, j, k))
#define SET3(arr, i, j, k, val) PyArray_SETITEM(arr, PyArray_GETPTR3(arr, i, j, k), PyFloat_FromDouble(val))
#define MIN(a, b) (a < b ? a : b)

void _get_coeff(float x_0, double* a, int a_len, int ord, PyArrayObject* coeff_arr){
	N = a_len;
	M = ord + 1;
	SET3(coeff_arr, 0, 0, 0, 1);

	c1 = 1;
	for (n = 1; n < N; n++){
		c2 = 1;
		m_min = MIN(n + 1, M);
		for (v = 0; v< n; v++){
			c3 = a[n] - a[v];
			c2 = c2 * c3;
			if (n < M) SET3(coeff_arr, n, n - 1, v, 0);
			for (m = 0; m < m_min; m++){
				d_1 = GET3(coeff_arr, m, n -1, v);
				d_2 = m == 0 ? 0 : GET3(coeff_arr, m - 1, n - 1, v);
				SET3(coeff_arr, m, n, v, ((a[n] - x_0) * d_1 - m * d_2) / c3);
			}
		}
		for (m = 0; m < m_min; m++){
			d_1 = m == 0? 0 : GET3(coeff_arr, m - 1, n - 1, n - 1);
			d_2 = GET3(coeff_arr, m, n - 1, n - 1);
			SET3(coeff_arr, m, n, n, (c1 / c2) * (m * d_1 - (a[n - 1] - x_0) * d_2));
		}
		c1 = c2;
	}
}

PyObject* get_coeff(PyObject* self, PyObject* args, PyObject* keywds){
	PyObject *a_obj;
	PyObject *coeff_arr_obj = NULL;
	PyArrayObject *a;
	PyArrayObject *coeff_arr;
	float x_0;
	int ord = 1;

	static char *kwlist[] = { "x_0", "a", "M", "coeff_arr", NULL };

	if (!PyArg_ParseTupleAndKeywords(args, keywds, "dO!|iO!", kwlist, &x_0, &PyArray_Type, &a_obj, &ord, &PyArray_Type, &coeff_arr_obj))
		return NULL;

	a_obj = PyArray_FROM_OTF(a_obj, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
	a = (PyArrayObject *)a_obj;

	// Check dims of `a`
	if (PyArray_NDIM(a) != 1) {
		PyErr_SetString(PyExc_ValueError, "Array `a` must be 1-dimensional");
		return NULL;
	}
	int a_len = PyArray_DIM(a, 0);
	npy_intp coeff_dims[] = {ord + 1, a_len, a_len};

	// Create a new array if not given coeff_arr
	coeff_arr_obj = coeff_arr_obj == NULL ? 
		PyArray_ZEROS(3, coeff_dims, NPY_DOUBLE, 0) :
		PyArray_FROM_OTF(coeff_arr_obj, NPY_DOUBLE, NPY_ARRAY_INOUT_ARRAY);
	coeff_arr = (PyArrayObject *)coeff_arr_obj;

	// Check shape of `coeff_arr`
	if (PyArray_NDIM(coeff_arr) != 3
		|| PyArray_DIM(coeff_arr, 0) != ord + 1
		|| PyArray_DIM(coeff_arr, 1) != a_len
		|| PyArray_DIM(coeff_arr, 2) != a_len) {
		PyErr_SetString(PyExc_ValueError, "Array `coeff_arr` must have shape [M + 1, N, N], where N is the length of `a`");
		return NULL;
	}

	double* a_ptr = (double *)PyArray_DATA(a);

	_get_coeff(x_0, a_ptr, a_len, ord, coeff_arr);
	return PyArray_Return(coeff_arr);
}


PyArrayObject* _derivate(PyArrayObject* x_arr, PyArrayObject* y_arr, int order, int accuracy){

	// Create result array
	npy_intp result_dims[] = { PyArray_DIM(y_arr, 0) - accuracy };
	PyArrayObject *result = (PyArrayObject*)PyArray_EMPTY(1, result_dims, NPY_DOUBLE, 0);
	double *x_data = (double *)PyArray_DATA(x_arr);
	double *y_data = (double *)PyArray_DATA(y_arr);
	int a_len = accuracy + 1;

	// Build coeff array
    npy_intp coeff_dims[] = { order + 1, a_len, a_len };
	PyArrayObject *coeff_arr = (PyArrayObject*)PyArray_EMPTY(3, coeff_dims, NPY_DOUBLE, 0);

	for (int i = 0; i < result_dims[0]; i++){
		// Get alpha values
		double *a = x_data + i;
		_get_coeff(x_data[i], a, a_len, order, coeff_arr);

		// Estimate derivative at x[i]
		double val = 0;
		for (int j = 0; j < a_len; j++){
			val += GET3(coeff_arr, order, a_len - 1, j) * y_data[i + j];
		}

		// Store result
		PyArray_SETITEM(result, PyArray_GETPTR1(result, i), PyFloat_FromDouble(val));
	}
	return result;
}


PyObject* derivate(PyObject* self, PyObject* args, PyObject* keywds){
	PyObject* x_arr_obj;
	PyObject* y_arr_obj;
	int order = 1;
	int accuracy = 1;

	static char *kwlist[] = { "x_arr", "y_arr", "order", "accuracy", NULL };

	if (!PyArg_ParseTupleAndKeywords(args, keywds, "O!O!|ii", kwlist, &PyArray_Type, &x_arr_obj, &PyArray_Type, &y_arr_obj, &order, &accuracy))
		return NULL;

	PyArrayObject* x_arr = (PyArrayObject*)PyArray_FROM_OTF(x_arr_obj, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
	PyArrayObject* y_arr = (PyArrayObject*)PyArray_FROM_OTF(y_arr_obj, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);

	// Check dims of `x_arr` and `y_arr`
	if (PyArray_NDIM(x_arr) != 1 || PyArray_NDIM(y_arr) != 1) {
		PyErr_SetString(PyExc_ValueError, "Array `x_arr` and `y_arr` must be 1-dimensional");
		return NULL;
	}

	// Check shape of `x_arr` and `y_arr`
	if (PyArray_DIM(x_arr, 0) != PyArray_DIM(y_arr, 0)) {
		PyErr_SetString(PyExc_ValueError, "Array `x_arr` and `y_arr` must have the same length");
		return NULL;
	}

	return PyArray_Return(_derivate(x_arr, y_arr, order, accuracy));
}


static PyMethodDef _fdce_methods[] = {
	{"get_coeff", (PyCFunction)get_coeff, METH_VARARGS | METH_KEYWORDS, "Get coefficients"},
	{"derivate", (PyCFunction)derivate, METH_VARARGS, "Derivate a function given a set of points"},
	{NULL, NULL, 0, NULL}
};


static struct PyModuleDef _fdce_module = {
	PyModuleDef_HEAD_INIT,
	"_fdce",
	NULL,
	-1,
	_fdce_methods
};

PyMODINIT_FUNC PyInit__fdce(void){
	PyObject *m = PyModule_Create(&_fdce_module);
	if (m == NULL)
		return NULL;
	import_array();
	return m;
}
