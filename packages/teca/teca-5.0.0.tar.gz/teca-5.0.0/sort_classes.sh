
rm geometry.rst \
    detector.rst \
    data_model.rst \
    processor.rst \
    execution.rst \
    io.rst \
    support.rst \
    calendar.rst \
    testing.rst

for f in `grep -zP  'class teca_[a-z_0-9:].*\n{' ./ -rIl --exclude-dir bin --exclude-dir build --exclude-dir test`;
do
    cname=`echo $f | cut -d/ -f3 | cut -d. -f1`;

    echo $cname

    read -p "data model:m detector:d geometry:g processor:p execution:e i/o:i support:s calendar:c test:t skip:q ?" -n 1 choice
    echo


    file=
    good=0
    while [[ ${good} == 0 ]]
    do
    case $choice in

        g)
            good=1
            file=geometry.rst
            ;;

        d)
            good=1
            file=detector.rst
            ;;

        m)
            good=1
            file=data_model.rst
            ;;
        p)
            good=1
            file=processor.rst
            ;;
        e)
            good=1
            file=execution.rst
            ;;
        i)
            good=1
            file=io.rst
            ;;
        s)
            good=1
            file=support.rst
            ;;
        c)
            good=1
            file=calendar.rst
            ;;
        t)
            good=1
            file=testing.rst
            ;;
        q)
            good=1
            ;;

    esac
    done

    echo ".. doxygenclass:: $cname"                    >> ${file}
    echo                                               >> ${file}
    echo '`'"$cname <./doxygen/class${cname}.html>"'`' >> ${file}

done

#.. doxygenclass:: 

