#ifndef buffer_h
#define buffer_h

/// @cond
/// A tag for dispatching operations on POD data
template <typename T>
struct pod_dispatch :
    std::integral_constant<bool,
    std::is_arithmetic<T>::value>
{};

/// A tag for disp[atching operations on classes
template <typename T>
struct object_dispatch :
    std::integral_constant<bool,
    !std::is_arithmetic<T>::value>
{};
/// @endcond

template <typename T>
using p_buffer = std::shared_ptr<T>;



///  a buffer that couuld be on the CPU or GPU
template <typename T>
class buffer : std::enable_shared_from_this<buffer<T>>
{
public:
    enum {
        ALLOC_NEW = 0,
        ALLOC_MALLOC = 1,
        ALLOC_CUDA_MALLOC = 2,
        ALLOC_CUDA_MALLOC_UVA = 2
    };

    /** allocates an empty and unitialized buffer that will use the declared
     * allocator. An allocator type must be declared to construct the buffer.
     */
    p_buffer<T> New(int alloc, size_t n_elem = 0, const data_t &val = data_t(),
        typename std::enable_if<pod_dispatch<T>::value>::type* = nullptr);

    /** allocates an empty and unitialized buffer that will use the declared
     * allocator. An allocator type must be declared to construct the buffer.
     */
    p_buffer<T> New(int alloc,
        typename std::enable_if<object_dispatch<T>::value>::type* = nullptr);





    /// returns the number of elelemts of storage allocated to the buffer
    size_t size() const { return n_size; }




    /// free all internall storage
    int free(typename std::enable_if<pod_dispatch<T>::value>::type* = nullptr);

    /// free all internall storage
    int free(typename std::enable_if<object_dispatch<T>::value>::type* = nullptr);




    /// allocates storage for n_elems of data
    int reserve(size_t n_elem,
        typename std::enable_if<pod_dispatch<T>::value>::type* = nullptr);

    /// allocates storage for n_elems of data
    int reserve(size_t n_elem,
        typename std::enable_if<object_dispatch<T>::value>::type* = nullptr);





    /// resizes storage for n_elems of data
    int resize(size_t n_elem,
        typename std::enable_if<pod_dispatch<T>::value>::type* = nullptr);

    /// resizes storage for n_elems of data
    int resize(size_t n_elem,
        typename std::enable_if<object_dispatch<T>::value>::type* = nullptr);




    /// appends a value at the end, extending the buffer as needed
    template <typename U>
    int append(const U &val,
        typename std::enable_if<pod_dispatch<T>::value>::type* = nullptr);

    /// appends a value at the end, extending the buffer as needed
    template <typename U>
    int append(const U &val,
        typename std::enable_if<object_dispatch<T>::value>::type* = nullptr);




    /// set the values of the buffer to a single value
    template <typename U>
    int set(const U &val, size_t start = 0, size_t end = 1,
        typename std::enable_if<pod_dispatch<T>::value>::type* = nullptr);

    /// set the values of the buffer to a single value
    template <typename U>
    int set(const U &val, size_t start = 0, size_t end = 1,
        typename std::enable_if<object_dispatch<T>::value>::type* = nullptr);




    /// set the values of the buffer to the values from another buffer
    /// start and end refer to elements in other,
    template <typename U>
    int set(const const_p_buffer<U> &other,
        size_t start = 0, size_t end = 1,
        typename std::enable_if<pod_dispatch<T>::value>::type* = nullptr);

    /// set the values of the buffer to the values from another buffer
    template <typename U>
    int set(const const_p_buffer &other,
        size_t start = 0, size_t end = 1,
        typename std::enable_if<object_dispatch<T>::value>::type* = nullptr);





    /// set the values of the buffer to the values from another buffer
    template <typename U>
    int set(const p_buffer &other, size_t start = 0, size_t end = 1,
        typename std::enable_if<pod_dispatch<T>::value>::type* = nullptr);

    /// set the values of the buffer to the values from another buffer
    template <typename U>
    int set(const p_buffer &other, size_t start = 0, size_t end = 1,
        typename std::enable_if<object_dispatch<T>::value>::type* = nullptr);









    /// 


    /// resizes the buffer, maintaining the current elements.
    

    /** retruns a pointer to the contents of the buffer accessible on the CPU
     * if the buffer is currently accessible by codes running on the CPU then
     * this call is a NOOP.  If the buffer is not currently accessible by codes
     * running on the CPU then a temporary buffer is allocated and the data is
     * moved to the CPU.  The returned shared_ptr deals with deallocation of
     * the temporary if needed.
     */
    template <typename U>
    std::shared_ptr<U> cpu_accessible();

    /** retruns a pointer to the contents of the buffer accessible by codes running on CUDA.
     * if the data is not accessible by codes running on CUDA then a temporarty buffer is allocated and
     * the data is moved to the CPU. The returned shared_ptr deals with
     * deallocation of the temprary.
     */
    template <typename U>
    std::shared_ptr<U> cuda_accessible() { return nullptr; }


    







protected:
    buffer(int alloc) : m_alloc(alloc) {}


    buffer() = delete;
    buffer(const buffer&) = delete;
    buffer(buffer&&) = delete;
    void operator(const buffer&) = delete;


private:
    int m_alloc;
    std::shared_ptr<T> m_data;
    size_t n_size;
    size_t n_capacity;
};

#endif
