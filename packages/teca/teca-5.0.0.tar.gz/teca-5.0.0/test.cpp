#include <iostream>
#include <sstream>
#include <cstring>
#include <vector>
using namespace std;

#define TECA_ERROR(_arg) \
std::cerr << _arg << std::endl;


template <typename d_type>
ostream &operator<<(ostream &os, const std::vector<d_type> &strs)
{
    size_t n = strs.size();
    for (size_t i = 0; i < n; ++i)
        os << strs[i] << ", ";
    return os;
}

int tokenize(char *istr, char delim, std::vector<char *> &ostr)
{
    // skip delim aqt the begining
    while ((*istr == delim) && (*istr != '\0'))
        ++istr;

    // nothing here
    if (*istr == '\0')
        return -1;

    // save the first
    ostr.push_back(istr);

    while (*istr != '\0')
    {
        while ((*istr != delim) && (*istr != '\0'))
            ++istr;

        if (*istr == delim)
        {
            // terminate the token
            *istr = '\0';
            ++istr;
            if (*istr != '\0')
            {
                // not at the end, start the next token
                ostr.push_back(istr);
            }
        }
    }
    return 0;
}

int skip_pad(char *&buf)
{
    while ((*buf != '\0') && ((*buf == ' ') || (*buf == '\n') || (*buf == '\r') || (*buf == '\t')))
        ++buf;
    return *buf == '\0' ? -1 : 0;
}

int is_comment(char *buf)
{
    skip_pad(buf);
    if (buf[0] == '#')
        return 1;
    return 0;
}



int main()
{
     char *csv =
R"_(# teca_table_writer_v2
# version descriptor
"pressure(10)" , "temperature(20)", "name(30)", "count(195)"
1.2, 2.2, "one", 2
1.3, 2.3, "two", 3
1.4, 2.4, "three", 4)_";

    size_t n_bytes = strlen(csv);
    char *buf = (char*)malloc(n_bytes+1);
    memcpy(buf, csv, n_bytes);
    buf[n_bytes] = '\0';

    /*char *cp = buf;
    char *ep = cp + strlen(buf);
    char *sb, *se, *np;
    while (str_field(cp, ep, sb, se, np) == 0)
    {
        std::string val(sb, se);
        std::cerr << val << std::endl;
        cp = np;
    }
    std::string val(sb, se);
    std::cerr << val << std::endl;
    cp = np;*/


    std::vector<char*> lines;
    if (tokenize(buf, '\n', lines))
    {
        TECA_ERROR("Failed to split lines")
        return -1;
    }
    size_t n_lines = lines.size();
    //std::cerr << "lines = {" << lines << "}" << std::endl;

    // skip comment lines
    size_t lno = 0;
    while ((lno < n_lines) && is_comment(lines[lno]))
        ++lno;

    // parse the header
    std::vector<char *> header;
    if (tokenize(lines[lno], ',', header))
    {
        TECA_ERROR("Failed to split fields")
        return -1;
    }

    // extract the name and type from each header field
    size_t n_cols = header.size();
    std::vector<std::string> col_names(n_cols);
    std::vector<int> col_types(n_cols);
    for (size_t i = 0; i < n_cols; ++i)
    {
        int n_match = 0;
        char name[128];
        int code = 0;
        if ((n_match = sscanf( header[i], " \"%128[^(](%d)\"", name, &code)) != 2)
        {
            TECA_ERROR("Failed to parse column name and type. " << n_match
                << " matches. Line " << lno << " column " << i << " field \""
                << header[i] << "\"")
            return -1;
        }
        col_names[i] = name;
        col_types[i] = code;
    }

    ++lno;

    std::cerr << "col_names = " << col_names << std::endl
        << "col_types = " << col_types << std::endl;

    for (; lno < n_lines; ++lno)
    {
        std::vector<char *> fields;
        if (tokenize(lines[lno], ',', fields))
        {
            TECA_ERROR("Failed to split fields")
            return -1;
        }
        std::cerr << lno << " fields = {" << fields << "}" << std::endl;
    }

    return 0;
}

