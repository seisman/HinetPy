Instrumental Response
=====================

Input
-----

The unit of Hi-net input is determined by column [9], ususally ``m/s``.

Analog Stage
------------

The moving coil velocity type seismometer is used in Hi-net and
its transfer function in the Laplace domain is given as:

.. math::

   \frac{Gs^2}{s^2 + 2hws + w^2}

where,

- :math:`G`: gain factor, given as column [8] in ``V/unit_of_input``
- :math:`h`: damping constant, given as column [11]
- :math:`w`: natural angular frequency, given as column [10]

Roots of the numerator and the denominator correspond to the
zeros and the poles, respectively, and the A0 normalization factor
is the inverse of the absolute value of the
above equation except G at the normalization frequency.

It's easy to know that the response has two poles and two zeros.
And A0 is equal to 2*[11].

Preamplification
----------------

The sensor ouput is amplified prior to A/D conversion.
The amplification factor is determined by column [12] in dB.

According to the definition of decibel of field quantities:

.. math::

   L_{F}=20\log _{10}\left({\frac {F}{F_{0}}}\right)\!~\mathrm {dB} .

Thus, the "sensitivity" in this stage is :math:`10^{\frac{[12]}{20}}` .

Analog-Digital Conversion
-------------------------

The gain in this stage is given by :math:`\frac{1}{[13]}`, in ``counts/V``.

Digital Stage
-------------

The gain in this stage is 1, according to the RESP file provided on Hi-net website.

Summary
-------

The total sensitivity is:

.. math::

    G = \frac{[8]*10^{\frac{[12]}{20}}}{[13]}

The ``CONSTANT`` in SAC PZ file is:

.. math::

    CONSTANT = A0 * G = 2 * [11] * \frac{[8]*10^{\frac{[12]}{20}}}{[13]}

Q&A
---

My question:

    Hi,

    I am using Hi-net data and am confused with the instrumental response
    even after I have looked through all pages of Hi-net website.

    In the page of 'For Registered Users' -> 'Response of Observation Equipment',
    only three RESP files are given. It seems that I have to rewrite a new RESP
    or SAC_PZ file for each channel.

    So I have to confirm that I understand details of response, which are very
    important for correct data processing.

    1. Do all channels have the same zeroes and poles?
    2. At line 19, do all channels have the same A0 Normalization factor (0.999953)?
    3. In the FAQ Q08, one equation is given to convert the A/D value from an WIN32
       file to the corresponding physical quantity. It is

            v = I * [13] / ([8] * 10 ^ ([12] / 20 ) )

       If I want to generate a SAC PZ file, the CONSTANT will be

        CONSTANT = [8]*10^([12]/20) / [13] * A0 ?

Answer from Hi-net:

    In the "Response of Observation Equipment" page, sample RESP files are
    provided and you need to modify them according to your purposes, as you
    wrote. The explanation in this page assumes that the parameters of the
    seismometer other than the gain factor do not change. Strictly speaking,
    the zeros, the poles, and the A0 normalization factor can change
    depending on the parameters of the seismometer. The moving coil velocity
    type seismometer is used in Hi-net and its transfer function in the
    Laplace domain is given as:

        Gs^2/(s^2 + 2hws + w^2)

    where G, h and w are the gain factor, the damping constant, and the
    natural angular frequency, respectively. Roots of the numerator and the
    denominator correspond to the zeros and the poles, respectively, and the
    A0 normalization factor is the inverse of the absolute value of the
    above equation except G at the normalization frequency. Detailed
    explanation about this type of seismometer is available in many
    literature, such as,

    Scherbaum, F., Of Poles and Zeros: Fundamentals of Digital Seismology,
    Kluwer Academic Publishers, 1996.
    #see chapter 4

    The gain factor, the damping constant, and the natural period are
    provided in the channels table file as explained in the Q&A08.
    Note that the gain factor is measured at its natural frequency.
    http://www.hinet.bosai.go.jp/faq/?LANG=en#Q08

    Please read the SEED manual about further details and SAC manual about
    SAC PZ file.

    - SEED: http://www.fdsn.org/publications.htm
    - SAC: http://www.iris.edu/files/sac-manual/

    Sincerely,

.. seealso::

   - `Hi-net FAQ 08 <http://www.hinet.bosai.go.jp/faq/?LANG=en#Q08>`_
   - `Response of Observation Equipment <https://hinetwww11.bosai.go.jp/auth/seed/?LANG=en>`_
