import pyinputplus as pypi

# Mengatur kerangka tampilan data di prompt 
formats = "{:<4}" + "{:<10}" * 4


def show(database, printFormat=formats, title="\nDaftar Buah yang Tersedia\n"):
    """Fungsi untuk menampilkan database ke prompt

    Args:
        database (dictionary): database yang akan ditampilkan
        printFormat (string): format tampilan di prompt
        title (str, optional): judul tampilan. Defaults "\nDaftar Buah yang Tersedia\n".
    """
    # Menampilkan judul
    print(title)
    # Loop item di dalam listFruit
    for value in database.values():
        # Menampilkan item berdasarkan format
        print(printFormat.format("", *value))
    print("\n")


def add(database):
    """Fungsi untuk menambahkan item ke dalam database

    Args:
        database (dict): database yang akan diolah

    Returns:
        dict: data terbaru
    """
    # Input nama item, validasi dengan regex numerik
    nameFruit = pypi.inputStr(
        prompt="Input nama item: ",
        applyFunc=lambda x: x.capitalize(),
        blockRegexes=[r"[0-9]"],
    )
    # Input jumlah item, validasi dengan integer number
    countFruit = pypi.inputInt(
        prompt="Input jumlah item: ",
    )
    # Input harga item, validasi dengan integer number
    priceFruit = pypi.inputInt(
        prompt="Input harga item: ",
    )
    # Apabila item tersedia, update stock atau harga item tersebut
    if nameFruit in list(database):
        database[nameFruit][2] += countFruit
        database[nameFruit][3] = priceFruit
    # Selain itu, tambahkan sebagai item baru
    else:
        database.update(
            {f"{nameFruit}": [len(database) - 1, nameFruit, countFruit, priceFruit]}
        )
    # Menampilkan daftar item terbaru
    show(database, formats)
    return database


def delete(database):
    """Fungsi untuk menghapus item dari database

    Args:
        database (dict): databases yang akan diolah

    Returns:
        dict: data terbaru
    """
    # Input indeks item yang akan dihapus
    # Validasi dengan indeks item yang tersedia
    id = pypi.inputInt(prompt="Input indeks item: ", lessThan=len(database) - 1)
    # Loop terhadap database
    for key, value in database.copy().items():
        if key == "column":
            continue
        # Jika item tersedia, hapus item berdasarkan indeks
        if id in value:
            del database[key]
        # Selain itu, update indeks item yang tersisa
        else:
            database.update({f"{key}": [value[0] - 1, value[1], value[2], value[3]]})
    # Menampilkan daftar item terbaru
    show(database, formats)
    return database


def buy(database):
    """Fitur untuk membeli item dari databases

    Args:
        database (dict): databases yang akan diolah

    Returns:
        dict: data terbaru
    """
    # Deklarasi variabel 'chart'
    chart = {
        "column": ["nama", "qty", "harga"],
    }
    while True:
        # Menampilkan data buah terbaru
        show(database, formats)
        # Input indeks item yang akan dibeli
        # Validasi dengan indeks item yang tersedia
        id = pypi.inputInt(prompt="Input indeks item: ", lessThan=len(database) - 1)
        # Breakdown item buah menjadi nama, stock, dan harga
        for value in database.values():
            if id in value:
                name, stock, price = value[1:]
                break
        # Input jumlah item, validasi dengan stock yang tersedia
        countFruit = pypi.inputInt(
            prompt="Input jumlah item: ",
            max=stock,
        )
        # Jika jumlah pesanan terpenuhi, update listChart
        chart.update({f"{name}": [name, countFruit, price]})
        # Kurangi persedian stock di database
        database[name][2] -= countFruit
        # Tampilkan isi keranjang belanjaan
        chartFormat = "{:<4}" + "{:<10}" * (len(chart["column"]))
        show(chart, chartFormat, title="\nIsi Keranjang Anda\n")
        # Konfirmasi status re-order
        reorder = pypi.inputYesNo(prompt="Beli item lain?(yes/no): ")
        if reorder.lower() == "no":
            break

    # Proses kalkulasi total harga
    for key, value in chart.items():
        if key == "column":
            # Tambah kolom 'total harga'
            value.append("total harga")
            chart[key] = value
        else:
            # Kalkulasi Qty x Harga
            value.append(value[1] * value[2])
            chart[key] = value

    # Proses pembayaran
    while True:
        # Menampilkan daftar belanja
        show(chart, formats, title="\nDaftar Belanjaan Anda\n")
        # Hitung total harga yang harus dibayar
        price = 0
        for value in list(chart.values())[1:]:
            price += value[-1]
        print(f"\nTotal yang harus dibayar: {price}")
        # Input jumlah uang pembayaran
        pay = pypi.inputInt(
            prompt="Input jumlah uang: ",
            min=price,
        )
        # Jika uang terpenuhi, tampilkan kembalian dan terima kasih
        print(f"Uang kembalian anda {pay - price}, terima kasih.")
        break
    # Kosongkan keranjang belanja
    del chart
    return database
