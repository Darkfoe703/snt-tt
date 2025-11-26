# app/cli/market_cli.py
import asyncio
import sys
from rich.console import Console
from rich.table import Table
from app.infrastructure.adapters.esi_adapter_market import ESIClientMarket

console = Console()

async def show_market_orders(region_id: int, type_id: int = None, order_type: str = "all"):
    """Función principal para mostrar órdenes de mercado"""
    client = ESIClientMarket()
    
    try:
        with console.status(f"[bold green]Obteniendo órdenes para región {region_id}..."):
            orders = await client.get_market_orders(region_id, type_id, order_type)
        
        if not orders:
            console.print(f"[yellow]No se encontraron órdenes en la región {region_id}[/yellow]")
            if type_id:
                console.print(f"[dim]Filtrado por tipo: {type_id}[/dim]")
            return
        
        # Crear tabla
        table = Table(
            title=f"Órdenes de Mercado - Región {region_id}",
            show_header=True,
            header_style="bold magenta"
        )
        table.add_column("Precio", style="cyan", justify="right")
        table.add_column("Volumen", style="green")
        table.add_column("Ubicación", style="yellow")
        table.add_column("Tipo", style="magenta")
        table.add_column("Rango", style="blue")
        
        for order in orders[:20]:  # Mostrar solo las primeras 20
            price = f"{order.get('price', 0):,.2f}"
            volume_remain = order.get('volume_remain', 0)
            volume_total = order.get('volume_total', 0)
            volume = f"{volume_remain:,}/{volume_total:,}"
            location = str(order.get('location_id', 'N/A'))
            order_type_display = "COMPRA" if order.get('is_buy_order', False) else "VENTA"
            range_val = order.get('range', 'station')
            
            table.add_row(price, volume, location, order_type_display, range_val)
        
        console.print(table)
        console.print(f"\n[bold]Total de órdenes:[/bold] {len(orders)}")
        if len(orders) > 20:
            console.print(f"[dim](Mostrando 20 de {len(orders)} órdenes)[/dim]")
            
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

def main():
    """CLI principal sin Typer - usando sys.argv directamente"""
    if len(sys.argv) < 2:
        console.print("[red]Uso: python -m app.cli.market_cli <region_id> [type_id] [order_type][/red]")
        console.print("\n[bold]Ejemplos:[/bold]")
        console.print("  python -m app.cli.market_cli 10000002")
        console.print("  python -m app.cli.market_cli 10000002 34")
        console.print("  python -m app.cli.market_cli 10000002 34 buy")
        return
    
    # Parsear argumentos
    region_id = int(sys.argv[1])
    type_id = None
    order_type = "all"
    
    if len(sys.argv) > 2:
        try:
            type_id = int(sys.argv[2])
        except ValueError:
            console.print(f"[yellow]type_id '{sys.argv[2]}' no es válido, ignorando...[/yellow]")
    
    if len(sys.argv) > 3:
        order_type = sys.argv[3]
    
    # Ejecutar
    asyncio.run(show_market_orders(region_id, type_id, order_type))

if __name__ == "__main__":
    main()