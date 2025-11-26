// app/infrastructure/api/web/static/js/table-sorter.js
class TableSorter {
    constructor(tableId) {
        this.table = document.getElementById(tableId);
        if (!this.table) {
            console.error(`No se encontró la tabla con id: ${tableId}`);
            return;
        }

        this.headers = this.table.querySelectorAll('thead th');
        this.currentSort = { column: -1, direction: 1 };
        this.init();
    }

    init() {
        this.headers.forEach((header, index) => {
            if (header.cellIndex >= 0) {
                header.style.cursor = 'pointer';
                header.style.position = 'relative';
                header.innerHTML = `↑↓ ${header.innerHTML}`;

                header.addEventListener('click', () => this.sortColumn(index));
            }
        });

        console.log('TableSorter inicializado para:', this.table.id);
    }

    sortColumn(columnIndex) {
        const tbody = this.table.querySelector('tbody');
        const rows = Array.from(tbody.querySelectorAll('tr'));

        // Determinar dirección de ordenamiento
        if (this.currentSort.column === columnIndex) {
            this.currentSort.direction *= -1;
        } else {
            this.currentSort.column = columnIndex;
            this.currentSort.direction = 1;
        }

        // Ordenar filas
        rows.sort((a, b) => {
            const aCell = a.cells[columnIndex];
            const bCell = b.cells[columnIndex];

            // Usar data-sort si está disponible, si no usar textContent
            let aValue = aCell.getAttribute('data-sort') || aCell.textContent.trim();
            let bValue = bCell.getAttribute('data-sort') || bCell.textContent.trim();

            // Convertir a números para ordenamiento correcto
            if (columnIndex >= 1 && columnIndex <= 6) { // Todas las columnas excepto "Item"
                aValue = this.parseNumber(aValue);
                bValue = this.parseNumber(bValue);
            }

            if (aValue < bValue) return -1 * this.currentSort.direction;
            if (aValue > bValue) return 1 * this.currentSort.direction;
            return 0;
        });

        // Limpiar tbody y agregar filas ordenadas
        while (tbody.firstChild) {
            tbody.removeChild(tbody.firstChild);
        }

        rows.forEach(row => tbody.appendChild(row));
        this.updateHeaders();
    }

    parseNumber(value) {
        if (value === null || value === undefined) return 0;

        // Para porcentajes
        if (typeof value === 'string' && value.includes('%')) {
            return parseFloat(value.replace('%', '')) || 0;
        }

        // Para números con formato
        const cleaned = value.toString().replace(/[^\d.-]/g, '');
        const parsed = parseFloat(cleaned);
        return isNaN(parsed) ? 0 : parsed;
    }

    updateHeaders() {
        this.headers.forEach((header, index) => {
            let symbol = '↑↓';
            if (index === this.currentSort.column) {
                symbol = this.currentSort.direction === 1 ? '↑' : '↓';
            }
            const text = header.textContent.replace(/[↑↓]/g, '').trim();
            header.innerHTML = `${symbol} ${text}`;
        });
    }
}

// Inicialización automática para tablas con la clase 'sortable'
document.addEventListener('DOMContentLoaded', function () {
    // Para tablas con ID específico
    const specificTable = document.getElementById('opportunities-table');
    if (specificTable) {
        new TableSorter('opportunities-table');
    }

    // Para cualquier tabla con clase 'sortable'
    document.querySelectorAll('table.sortable').forEach(table => {
        if (table.id) {
            new TableSorter(table.id);
        } else {
            // Generar un ID único si no tiene
            const uniqueId = 'table-' + Math.random().toString(36).substr(2, 9);
            table.id = uniqueId;
            new TableSorter(uniqueId);
        }
    });
});