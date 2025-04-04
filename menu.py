import flet as ft
from time import sleep
from subajuda import pedido,consulta_bd,lanche,porcao

def main(page:ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 550
    def abrir_principal(e):
        page_principal.col['xs']=12
        page_artesanais.col['xs']=0
        tela_de_pedidos.col['xs']=0 
        page.update()
    def abrir_arte(e):
        page_principal.col['xs']=0
        page_artesanais.col['xs']=12
        tela_de_pedidos.col['xs']=0 
        page.update()
        
    def fazer_pedido(e):
        page_principal.col['xs']=0
        page_artesanais.col['xs']=0
        tela_de_pedidos.col['xs']=12
        page.update()
    
    def enviar_pedidos(e):
        if campo_lista.content.controls[1].content.controls==[]:
            mensagem(text='desculpa, más não tem como enviar o pedido com a lista vazia!')
        elif nome.content.controls[1].disabled == False:
            mensagem(text='por favor insira seu nome para que possamos te atender melhor.')
        elif campo_mesa.controls[1].disabled==False:
            mensagem(text='por favor selecione em qual mesa esta para que possamos te atender melhor.')
        else:
            pedido=''
            for item in campo_lista.content.controls[1].content.controls:
                pedido+=f'{item.controls[0].content.value}\n'
            pedido+=f'{total.controls[0].value}{total.controls[1].value}'
            campo_lista.content.controls[1].content.controls=None
            total.controls[1].value = 0
            campo_mesa.controls[1].disabled=False
            campo_mesa.controls[2].disabled=False
            nome.content.controls[1].disabled=False
            nome.content.controls[2].disabled=False
            nome.update()
            campo_mesa.update()
            total.update()
            campo_lista.update()
            mensagem(text='Pedido Enviado Com Sucesso!')
            consulta_bd(sql="INSERT INTO todos_pedidos ( pedido ) VALUES ( %s)",valores=(pedido,))
            print('enviou com sucesso')
    
    def adiciona_item(e):
        if e.control.parent.controls[0].value == None or e.control.parent.controls[1].content.value == None:
            mensagem(text='Por Favor Você Deve Selecionar A Quantidade E O Pedido Desejado Na Lista De Pedidos')
        else:
            string=f'{e.control.parent.controls[0].value} - {e.control.parent.controls[1].content.value}'
            separa=string.split()
            numero = float(e.control.parent.controls[0].value[0])
            real = float(separa[-1])
            dinheiro = real * numero
            numero_final=float(total.controls[1].value + dinheiro)
            total.controls[1].value=round(numero_final,2)
            total.update()
            string_2=f'{e.control.parent.controls[0].value} - {separa[2]} {separa[3]} {round(dinheiro,2)}'
            pedido=ft.ResponsiveRow(
                    columns=12,
                    controls=[
                        ft.Container(
                            content=ft.Text(value=string_2,color=ft.colors.YELLOW_600,weight=ft.FontWeight.BOLD,size=20),
                            bgcolor=ft.colors.with_opacity(color=ft.colors.BLACK,opacity=1.0),
                            shadow=ft.BoxShadow(blur_radius=5,color=ft.colors.YELLOW_ACCENT_700),
                            padding=ft.padding.only(left=15,right=15,bottom=5,top=5),
                            border_radius=ft.border_radius.all(10),
                            col={'xs':10}
                                ),
                        ft.Container(
                            content=ft.Image(
                                src='deleta.png'
                            ),width=50,height=50,col={'xs':2},on_click=excluir_item
                        )
                    ]
            )
            
            campo_lista.content.controls[1].content.controls.append(pedido)
            
            campo_lista.update()
            campo_lanches.controls[0].value = None
            campo_lanches.controls[1].content.value=None
            campo_lanches.update()
            campo_artesanais.controls[0].value = None
            campo_artesanais.controls[1].content.value=None
            campo_artesanais.update()
            campo_bebidas.controls[0].value = None
            campo_bebidas.controls[1].content.value=None
            campo_bebidas.update()
            campo_combos.controls[0].value = None
            campo_combos.controls[1].content.value=None
            campo_combos.update()
            campo_porcoes.controls[0].value = None
            campo_porcoes.controls[1].content.value=None
            campo_porcoes.update()
            mensagem(text='Pedido Adicionado Na Lista De Pedidos Com Sucesso!')
    def exclui_nome(e):
        for item in campo_lista.content.controls[1].content.controls:
            if item.controls[0].content.value == e.control.parent.controls[0].content.value:
                campo_lista.content.controls[1].content.controls.remove(item)
                nome.content.controls[1].disabled=False
                nome.content.controls[2].disabled=False
                nome.update()
                campo_lista.update()
                break
        mensagem(text='Nome Excluído\nCom Sucesso!')
    def excluir_item(e):
        for item in campo_lista.content.controls[1].content.controls:
            if item.controls[0].content.value == e.control.parent.controls[0].content.value:
                campo_lista.content.controls[1].content.controls.remove(item)
                string=item.controls[0].content.value
                separa=string.split()
                real = float(separa[-1])
                numero_final=float(total.controls[1].value - real)
                total.controls[1].value=round(numero_final,2)
                total.update()
                campo_lista.update()
                break
        mensagem(text='Pedido Excluido Com Suceso!')
    def mensagem(text):
        msg = ft.AlertDialog(
                    title=ft.Text(value=text),
                    title_padding=ft.padding.all(50),
                    open=True
                )
        page.add(msg)
        sleep(5)
        msg.open=False
        page.update()
    
    def excluir_mesa(e):
        for item in campo_lista.content.controls[1].content.controls:
            if item.controls[0].content.value == e.control.parent.controls[0].content.value:
                campo_lista.content.controls[1].content.controls.remove(item)
                campo_mesa.controls[1].disabled=False
                campo_mesa.controls[2].disabled=False
                campo_mesa.update()
                campo_lista.update()
                break
        mensagem(text='Mesa Excluída\nCom Cucesso!')
    
    def adiciona_mesa(e):
        mesa=ft.ResponsiveRow(
                        columns=12,
                        controls=[
                            ft.Container(
                                content=ft.Text(value=f'MESA N°: {campo_mesa.controls[1].value}'.upper(),color=ft.colors.YELLOW_600,weight=ft.FontWeight.BOLD,size=20),
                                bgcolor=ft.colors.with_opacity(color=ft.colors.BLACK,opacity=1.0),
                                shadow=ft.BoxShadow(blur_radius=5,color=ft.colors.YELLOW_ACCENT_700),
                                padding=ft.padding.only(left=15,right=15,bottom=5,top=5),
                                border_radius=ft.border_radius.all(10),
                                col={'xs':10}
                                    ),
                            ft.Container(
                                content=ft.Image(
                                    src='deleta.png'
                                ),width=50,height=50,col={'xs':2},on_click=excluir_mesa
                            )
                        ]
                )
        if campo_mesa.controls[1].value == None:
            mensagem(text='Por Favor Selecione Uma Opção Para Adicionar Na Lista De Pedidos')
        elif nome.content.controls[1].disabled == True:
            campo_lista.content.controls[1].content.controls.insert(1,mesa)
            campo_mesa.controls[1].disabled=True
            campo_mesa.controls[2].disabled=True
            campo_mesa.controls[1].value = None
            campo_mesa.update()
            campo_lista.update()
            mensagem(text='Mesa Acicionada\n Com Sucesso!')
        elif nome.content.controls[1].disabled == False:
            campo_lista.content.controls[1].content.controls.insert(0,mesa)
            campo_mesa.controls[1].disabled=True
            campo_mesa.controls[2].disabled=True
            campo_mesa.controls[1].value = None
            campo_mesa.update()
            campo_lista.update()
            mensagem(text='Mesa Acicionada\n Com Sucesso!')
            
    def adicionar_nome(e):
        stri=e.control.parent.controls[1].value.replace(" ","")
        if stri == '':
            mensagem(text='Por Favor Digite Seu Nome Para Que Seja Adicionado Na Lista De Pedidos')
        else:
            n=ft.ResponsiveRow(
                            columns=12,
                            controls=[
                                ft.Container(
                                    content=ft.Text(value=f'CLIENTE: {nome.content.controls[1].value}'.upper(),color=ft.colors.YELLOW_600,weight=ft.FontWeight.BOLD,size=20),
                                    bgcolor=ft.colors.with_opacity(color=ft.colors.BLACK,opacity=1.0),
                                    shadow=ft.BoxShadow(blur_radius=5,color=ft.colors.YELLOW_ACCENT_700),
                                    padding=ft.padding.only(left=15,right=15,bottom=5,top=5),
                                    border_radius=ft.border_radius.all(10),
                                    col={'xs':10}
                                        ),
                                ft.Container(
                                    content=ft.Image(
                                        src='deleta.png'
                                    ),width=50,height=50,col={'xs':2},on_click=exclui_nome
                                )
                            ]
                    )
            campo_lista.content.controls[1].content.controls.insert(0,n)
            campo_lista.update()
            nome.content.controls[1].value = ''
            nome.content.controls[1].disabled=True
            nome.content.controls[2].disabled=True
            nome.update()
            mensagem(text='Nome Adicionado\n Na Lista De Pedido\nCom Sucesso!')
            
    
    
    
    
    logo_pedidos=ft.Container(
        border_radius=ft.border_radius.all(10),
        bgcolor=ft.colors.BLACK,
        height=180,
        expand=True,
        alignment=ft.alignment.top_center,
        content=ft.Image(
            src='pedidos.png',
            fit=ft.ImageFit.FILL
        )
    )
        
    nome = ft.Container(
        padding=10,
        content=ft.Row(
            wrap=True,
            controls=[
                ft.Text(
                    value='nome:'.upper(),
                    size=15,
                    italic=True,
                    weight=ft.FontWeight.BOLD
                ),
                ft.TextField(
                    hint_text='Ex: LUCAS',
                    multiline=True,
                    max_lines=2,
                    width=232,
                    hint_style=ft.TextStyle(color=ft.colors.WHITE,italic=True,weight=ft.FontWeight.BOLD),
                    border_color=ft.colors.WHITE,
                    disabled=False
                ),
                ft.Container(
               width=50,
               height=40,
               bgcolor=ft.colors.ORANGE,
               border_radius=ft.border_radius.all(10),
               padding=ft.padding.symmetric(horizontal=5),
               content=ft.Image(
                   src='concluido.png',
                   fit=ft.ImageFit.COVER
               ),on_click=adicionar_nome
               )
            ]
        )
    )
       
    campo_lanches=ft.Row(
        wrap=True,
        controls=[
            ft.Dropdown(
                label='QTD',
                border_color=ft.colors.WHITE,
                border_width=0.8,
                width=60,
                options=[
                    ft.dropdown.Option(text=f'{num}x')for num in range(1,11)
                ]
                ),
            ft.Container(
        content=ft.Dropdown(
            label='L/TRADICIONAIS',
            border_color=ft.colors.WHITE,
            width=240,
            icon_size=0,
            border_width=0.8,
            padding=ft.padding.symmetric(horizontal=5),
            alignment=ft.alignment.center_left,
            options=[
                ft.dropdown.Option(text='hamburguinho  R$ 10.00'.upper()),
                ft.dropdown.Option(text='x-calabresa  R$ 19.99'.upper()),
                ft.dropdown.Option(text='x-Bacon  R$ 19.99'.upper()),
                ft.dropdown.Option(text='x-frangão  R$ 19.99'.upper()),
                ft.dropdown.Option(text='x-mamãe  R$ 35.00'.upper()),
            ]
        )
    ),
           ft.Container(
               width=50,
               height=40,
               bgcolor=ft.colors.ORANGE,
               border_radius=ft.border_radius.all(10),
               padding=ft.padding.symmetric(horizontal=5),
               content=ft.Image(
                   src='concluido.png',
                   fit=ft.ImageFit.COVER
               ),
               on_click=adiciona_item
           )
        ]
    )
    
    campo_artesanais=ft.Row(
        wrap=True,
        controls=[
            ft.Dropdown(
                label='QTD',
                text_size=10,
                border_color=ft.colors.WHITE,
                border_width=0.8,
                width=60,
                options=[
                    ft.dropdown.Option(text=f'{num}x')for num in range(1,11)
                ]
                ),
            ft.Container(
        content=ft.Dropdown(
            label='L/artesanais'.upper(),
            border_color=ft.colors.WHITE,
            width=240,
            icon_size=0,
            border_width=0.8,
            padding=ft.padding.symmetric(horizontal=5),
            alignment=ft.alignment.center_left,
            options=[
                ft.dropdown.Option(text='farol  R$ 23.00'.upper()),
                ft.dropdown.Option(text='frango especial  R$ 24.00'.upper()),
                ft.dropdown.Option(text='nativo  R$ 25.00'.upper()),
                ft.dropdown.Option(text='atanagildo  R$ 28.00'.upper()),
                ft.dropdown.Option(text='crumaí  R$ 34.99'.upper()),
            ]
        )
    ),
           ft.Container(
               width=50,
               height=40,
               bgcolor=ft.colors.ORANGE,
               border_radius=ft.border_radius.all(10),
               padding=ft.padding.symmetric(horizontal=5),
               content=ft.Image(
                   src='concluido.png',
                   fit=ft.ImageFit.COVER
               ),
               on_click=adiciona_item
           )
        ]
    )
    campo_combos=ft.Row(
        wrap=True,
        controls=[
            ft.Dropdown(
                label='QTD',
                border_color=ft.colors.WHITE,
                border_width=0.8,
                width=60,
                options=[
                    ft.dropdown.Option(text=f'{num}x')for num in range(1,6)
                ]
                ),
            ft.Container(
        content=ft.Dropdown(
            label='combos'.upper(),
            border_color=ft.colors.WHITE,
            width=240,
            icon_size=0,
            border_width=0.8,
            padding=ft.padding.symmetric(horizontal=5),
            alignment=ft.alignment.center_left,
            options=[
                ft.dropdown.Option(text='combinho kids  R$ 25.00'.upper()),
                ft.dropdown.Option(text='combo barra 2  R$ 70.00'.upper()),
            ]
        )
    ),
            ft.Container(
               width=50,
               height=40,
               bgcolor=ft.colors.ORANGE,
               border_radius=ft.border_radius.all(10),
               padding=ft.padding.symmetric(horizontal=5),
               content=ft.Image(
                   src='concluido.png',
                   fit=ft.ImageFit.COVER
               ),
               on_click=adiciona_item
           )
        ]
    )
    campo_bebidas=ft.Row(
        wrap=True,
        controls=[
            ft.Dropdown(
                label='QTD',
                border_color=ft.colors.WHITE,
                border_width=0.8,
                width=60,
                options=[
                    ft.dropdown.Option(text=f'{num}x')for num in range(1,11)
                ]
                ),
            ft.Container(
        content=ft.Dropdown(
            label='bebidas'.upper(),
            border_color=ft.colors.WHITE,
            width=240,
            icon_size=0,
            border_width=0.8,
            padding=ft.padding.symmetric(horizontal=5),
            alignment=ft.alignment.center_left,
            options=[
                ft.dropdown.Option(text='suco copo  R$ 5.99'.upper()),
                ft.dropdown.Option(text='refrigerante Lata R$ 5.99'.upper()),
                ft.dropdown.Option(text='refrigerante 1 lt  R$ 9.99'.upper()),
                ft.dropdown.Option(text='refrigerante 2 lt  R$ 15.99'.upper()),
                ft.dropdown.Option(text='água 500 ml  R$ 3.99'.upper()),
                ft.dropdown.Option(text='água c/gás 500 ml  R$ 4.99'.upper()),
            ]
        )
    ),
            ft.Container(
               width=50,
               height=40,
               bgcolor=ft.colors.ORANGE,
               border_radius=ft.border_radius.all(10),
               padding=ft.padding.symmetric(horizontal=5),
               content=ft.Image(
                   src='concluido.png',
                   fit=ft.ImageFit.COVER
               ),
               on_click=adiciona_item
           )
        ]
    )
    campo_porcoes=ft.Row(
        wrap=True,
        controls=[
            ft.Dropdown(
                label='QTD',
                border_color=ft.colors.WHITE,
                border_width=0.8,
                width=60,
                options=[
                    ft.dropdown.Option(text=f'{num}x')for num in range(1,11)
                ]
                ),
            ft.Container(
        content=ft.Dropdown(
            label='porções'.upper(),
            width=240,
            icon_size=0,
            border_color=ft.colors.WHITE,
            border_width=0.8,
            padding=ft.padding.symmetric(horizontal=5),
            alignment=ft.alignment.center_left,
            options=[
                ft.dropdown.Option(text='batata frita c/bacon  R$ 29.99'.upper()),
                ft.dropdown.Option(text='batata frita c/calabresa  R$ 29.99'.upper()),
                ft.dropdown.Option(text='batata frita c/cheddar R$ 29.99'.upper()),
                ft.dropdown.Option(text='batata frita c/catupiry R$ 29.99'.upper()),
                ft.dropdown.Option(text='batata frita completa R$ 39.99'.upper()),
            ]
        )
    ),
            ft.Container(
               width=50,
               height=40,
               bgcolor=ft.colors.ORANGE,
               border_radius=ft.border_radius.all(10),
               padding=ft.padding.symmetric(horizontal=5),
               content=ft.Image(
                   src='concluido.png',
                   fit=ft.ImageFit.COVER
               ),
               on_click=adiciona_item
           )
        ]
    )
    campo_lista=ft.Container(
        bgcolor=ft.colors.BLACK12,
        padding=ft.padding.only(left=30,right=30,top=10,bottom=10),
        alignment=ft.alignment.top_center,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    content=ft.Text(value='lista de pedido'.upper(),color=ft.colors.YELLOW_600,weight=ft.FontWeight.BOLD,size=20),
                    bgcolor=ft.colors.with_opacity(color=ft.colors.BLACK,opacity=1.0),
                    shadow=ft.BoxShadow(blur_radius=5,color=ft.colors.YELLOW_ACCENT_700),
                    padding=ft.padding.only(left=15,right=15,bottom=5,top=5),
                    border_radius=ft.border_radius.all(20),
                        ),
                ft.Container(
                    height=400,
                    width=400,
                    padding=ft.padding.symmetric(vertical=20,horizontal=20),
                    bgcolor=ft.colors.with_opacity(color=ft.colors.BLACK12,opacity=1.0),
                    border_radius=ft.border_radius.all(20),
                    shadow=ft.BoxShadow(blur_radius=5,color=ft.colors.YELLOW_ACCENT_700),
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        scroll=ft.ScrollMode.HIDDEN,
                        spacing=10,
                        width=500,
                        controls=[
                        ]
                    )
                )
            ]
        )
    )
    campo_mesa = ft.Row(
        wrap=True,
        controls=[
            ft.Text(
                value='n° mesa:'.upper(),
                weight=ft.FontWeight.BOLD,
                italic=True,
                size=15,
                col=4,
                text_align=ft.TextAlign.CENTER,
                offset=ft.Offset(x=0,y=-0.3)
            ),
            ft.Dropdown(
                label='Numero da mesa'.upper(),
                label_style=ft.TextStyle(color=ft.colors.WHITE,italic=True,weight=ft.FontWeight.BOLD),
                col=6,
                width=230,
                icon_size=0,
                border_color=ft.colors.WHITE,
                border_width=0.8,
                options=[
                    ft.dropdown.Option('1'),
                    ft.dropdown.Option('2'),
                    ft.dropdown.Option('3'),
                    ft.dropdown.Option('4'),
                    ft.dropdown.Option('5'),
                    ft.dropdown.Option('não estou em uma mesa'.upper()),
                ]
                ),
            ft.Container(
                height=40,
                width=50,
               col=1.7,
               bgcolor=ft.colors.ORANGE,
               border_radius=ft.border_radius.all(10),
               padding=ft.padding.symmetric(horizontal=5),
               content=ft.Image(
                   src='concluido.png',
                   fit=ft.ImageFit.COVER,
                   
               ),on_click=adiciona_mesa
           )
            
        ]
    )
    
    total = ft.Row(
        alignment=ft.alignment.top_center,
        offset=ft.Offset(x=0.3,y=0),
        controls=[
            ft.Text(
                value='total R$:'.upper(),
                weight=ft.FontWeight.BOLD,
                size=20,
                italic=True,
            ),
            ft.Text(
                value=0,
                weight=ft.FontWeight.BOLD,
                size=20,
                italic=True,
            )
        ]
    )
    enviar_pedido=ft.ElevatedButton(
        width=900,
        text='enviar pedido'.upper(),
        style=ft.ButtonStyle(
            padding=ft.padding.all(20),
            text_style=ft.TextStyle(size=20,weight=ft.FontWeight.BOLD,color=ft.colors.WHITE),
        ),
        color=ft.colors.WHITE,
        on_click=enviar_pedidos
    )
    footer=ft.Container(
        padding=ft.padding.symmetric(vertical=20),
        content=ft.ResponsiveRow(
            columns=12,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
               ft.Container(
                   bgcolor=ft.colors.BLACK,
                   alignment=ft.alignment.center,
                   width=250,
                   col={'md':6,'lg':6,'xs':5},
                   url='https://www.instagram.com/mamae_lanches_e_drinks_/',
                   offset=ft.Offset(x=-0.2,y=0),
                   content=ft.Column(
                       horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                       controls=[
                           ft.Image(
                               src='insta.jpg',
                               width=60,
                               height=70,
                               fit=ft.ImageFit.FILL
                           ),
                           ft.Text(
                               value='@mamae_lanches_e_drinks',
                               italic=True,
                               weight=ft.FontWeight.BOLD,
                               color=ft.colors.WHITE,
                               #offset=ft.Offset(x=-0.6,y=0),
                               no_wrap=True,
                               expand=True
                           )
                       ]
                   )
               ),
               ft.Container(
                   bgcolor=ft.colors.BLACK,
                   alignment=ft.alignment.center,
                   offset=ft.Offset(x=0.3,y=0.1),
                   col={'md':6,'lg':6,'xs':5},
                   url='https://wa.me/<5575998611227>',
                   content=ft.Column(
                       controls=[
                           ft.Image(
                               src='whatsapp.png',
                               width=60,
                               height=60,
                               fit=ft.ImageFit.FILL
                           ),
                           ft.Text(
                               value='75 998621227',
                               italic=True,
                               weight=ft.FontWeight.BOLD,
                               color=ft.colors.WHITE,
                               offset=ft.Offset(x=-0.2,y=-0.2)
                           )
                       ]
                   )
               )
            ]
        )
    )


        
    button_artesanais = ft.Container(
        padding=ft.padding.only(top=5,right=30),
        content=ft.ResponsiveRow(
            controls=[
                ft.Container(
                    content=ft.Text(value='menu l/artesanal'.upper(),color=ft.colors.YELLOW_600,weight=ft.FontWeight.BOLD),
                    bgcolor=ft.colors.with_opacity(color=ft.colors.BLACK,opacity=1.0),
                    offset=ft.Offset(y=0.0,x=0.1),
                    shadow=ft.BoxShadow(blur_radius=5,color=ft.colors.YELLOW_ACCENT_700),
                    padding=ft.padding.only(left=15,right=15,bottom=5,top=5),
                    border_radius=ft.border_radius.all(20),
                    on_click=abrir_arte,
                    alignment=ft.alignment.center,
                    col={'xs':6}
                    ),
                ft.Container(
                    content=ft.Text(value='menu l/principal'.upper(),color=ft.colors.YELLOW_600,weight=ft.FontWeight.BOLD),
                    bgcolor=ft.colors.with_opacity(color=ft.colors.BLACK,opacity=1.0),
                    offset=ft.Offset(y=0.0,x=0.1),
                    shadow=ft.BoxShadow(blur_radius=5,color=ft.colors.YELLOW_ACCENT_700),
                    padding=ft.padding.only(left=15,right=15,bottom=5,top=5),
                    border_radius=ft.border_radius.all(20),
                    on_click=abrir_principal,
                    alignment=ft.alignment.center,
                    col={'xs':6}
                    ),
                ft.Container(
                    content=ft.Text(value='fazer pedido'.upper(),color=ft.colors.YELLOW_600,weight=ft.FontWeight.BOLD),
                    bgcolor=ft.colors.with_opacity(color=ft.colors.BLACK,opacity=1.0),
                    offset=ft.Offset(y=0.0,x=0.1),
                    shadow=ft.BoxShadow(blur_radius=5,color=ft.colors.YELLOW_ACCENT_700),
                    padding=ft.padding.only(left=15,right=15,bottom=5,top=5),
                    border_radius=ft.border_radius.all(20),
                    on_click=fazer_pedido,
                    alignment=ft.alignment.center,
                    col={'xs':6}
                    ),
            ]
        )
    )
    logo = ft.Container(
        content=ft.Image(
            src='logo.jpg',
            expand=True,
            fit=ft.ImageFit.COVER
            ),
        padding=2,
        border_radius=ft.border_radius.all(15),
        bgcolor=ft.colors.BLACK,
        expand=True
    )
    lanches = ft.Container(
        content=ft.Column(
            controls=[
                button_artesanais,
                lanche(nome='farol',preco='23,00',receita='Pão da casa: Carne 100g, Queijo, Presunto, Bacon-Triturado, Tomate, Alfaçe, Molho.'),
                lanche(nome='frango especial',preco='24,00',receita='Pão da casa, Carne 100g, Frango, Queijo, Catupiry, Tomate, Alface, Molho.'),
                lanche(nome='nativo',preco='25,00',receita='Pão da casa, Carne 100g, Calabresa, Quejo, Ovo, Cebola Caramelizada, Tomate, Alface, Molho.'),
                lanche(nome='atanagildo', preco='28,00',receita='Pão da casa, Carne 100g, Farofa de Calabresa e Bacon, Queijo, Presunto, Ovo, Tomate, Alface, Molho.'),
                lanche(nome='crumaí',preco='34,99',receita='Pão da casa, 2 Carne 100g, Calabresa, Bacon, Frango, Cheddar, Cebola caramelizada, Tomate, Alface, Molho.'),
              adiocionais := ft.Container(
        shadow=ft.BoxShadow(blur_radius=10,color=ft.colors.WHITE12),
        alignment=ft.alignment.top_center,
        padding=ft.padding.only(left=10,bottom=10,right=10),
        content=ft.Column(
            controls=[
                ft.ResponsiveRow(
                    col=12,
                    spacing=0,
                    controls=[
                        ft.Container(
                            content=ft.IconButton(
                                icon=ft.icons.ARROW_FORWARD,
                                icon_color=ft.colors.YELLOW,
                                height=20                            
                            ),
                            col=1,
                            offset=ft.Offset(x=0.0,y=-0.5)
                            ),
                        ft.Text(
                            value= 'Adicionais'.upper(),
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.YELLOW,
                            col=5
                        ),
                        ft.Text(
                                value=f'R$ 4,00 ',
                            col=3,
                            color=ft.colors.LIGHT_GREEN_ACCENT_400,
                            weight=ft.FontWeight.W_700
                        )
                    ]
                )
            ],
            
        )
    )
                
        ]
    ))
    combos = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text(
                    value='combos'.upper(),
                    text_align=ft.TextAlign.CENTER,
                    style=ft.TextStyle(font_family=ft.colors.BLACK26,italic=True,weight=ft.FontWeight.W_900,size=60,color=ft.colors.RED_ACCENT_700,decoration_color=ft.colors.WHITE),
                    weight=ft.FontWeight.W_900
                    
                ),
                    padding=ft.padding.symmetric(horizontal=50,vertical=20),
                    alignment=ft.alignment.top_center
                    
                ),
                ft.Container(
                    shadow=ft.BoxShadow(blur_radius=15,color=ft.colors.WHITE12),
                    padding=ft.padding.symmetric(horizontal=15,vertical=15),
                    content=ft.Column(
                        spacing=-2,
                        controls=[
                            ft.Text(
                    text_align=ft.alignment.bottom_left,
                    spans=[
                        ft.TextSpan(text='COMBINHO KIDS',style=ft.TextStyle(color=ft.colors.YELLOW,weight=ft.FontWeight.W_900,size=30)),
                        ft.TextSpan(text='  R$ 25,00',style=ft.TextStyle(color=ft.colors.LIGHT_GREEN_ACCENT_700,weight=ft.FontWeight.W_900,size=30)),
                    ]
                ),
                            ft.Text(
                                offset=ft.Offset(y=0,x=0.05),
                                
                    text_align=ft.alignment.bottom_left,
                    spans=[
                        ft.TextSpan(text='1 Sanduiche com',style=ft.TextStyle(color=ft.colors.RED_600,weight=ft.FontWeight.BOLD,size=25)),
                        ft.TextSpan(text=': Pão da Casa, C/Hambúrguer, Quejo, Presunto, Tomate, Alface.',style=ft.TextStyle(color=ft.colors.WHITE,weight=ft.FontWeight.BOLD,size=25)),
                    ]
                ),
                            ft.Text(
                    text_align=ft.alignment.bottom_left,
                    offset=ft.Offset(y=0,x=0.05),
                    spans=[
                        ft.TextSpan(text='Suco/Refrigerante',style=ft.TextStyle(color=ft.colors.GREEN_600,weight=ft.FontWeight.BOLD,size=25)),
                        ft.TextSpan(text=' De 250 ML',style=ft.TextStyle(color=ft.colors.WHITE,weight=ft.FontWeight.BOLD,size=25)),
                    ]
                ),
                            ft.Text(
                                value='Batata Palha',
                                size=25,
                                color=ft.colors.WHITE,
                                offset=ft.Offset(y=0,x=0.19),
                                weight=ft.FontWeight.BOLD
                            ),
                            ft.Text(
                                value='+Brinde',
                                size=25,
                                color=ft.colors.RED_600,
                                offset=ft.Offset(y=0,x=0.35),
                                weight=ft.FontWeight.BOLD
                            )
                        ]
                    )
                ),
                ft.Container(
                    shadow=ft.BoxShadow(blur_radius=15,color=ft.colors.WHITE12),
                    padding=ft.padding.symmetric(horizontal=15,vertical=15),
                    content=ft.Column(
                        spacing=-2,
                        controls=[
                            ft.Text(
                    text_align=ft.alignment.bottom_left,
                    spans=[
                        ft.TextSpan(text='COMBO BARRA 2',style=ft.TextStyle(color=ft.colors.YELLOW,weight=ft.FontWeight.W_900,size=30)),
                        ft.TextSpan(text=' R$ 70,00',style=ft.TextStyle(color=ft.colors.LIGHT_GREEN_ACCENT_700,weight=ft.FontWeight.W_900,size=30)),
                    ]
                ),
                            ft.Text(
                                offset=ft.Offset(y=0,x=0.05),
                                
                    text_align=ft.alignment.bottom_left,
                    spans=[
                        ft.TextSpan(text='2 Sanduiches com',style=ft.TextStyle(color=ft.colors.RED_600,weight=ft.FontWeight.BOLD,size=25)),
                        ft.TextSpan(text=': Pão da Casa, Carne 100g, Farofa de Calabresa e Bacon, Quejo, Presunto, Ovo, Tomate, Alface, Molho.',style=ft.TextStyle(color=ft.colors.WHITE,weight=ft.FontWeight.BOLD,size=25)),
                    ]
                ),
                            ft.Text(
                    text_align=ft.alignment.bottom_left,
                    offset=ft.Offset(y=0,x=0.05),
                    spans=[
                        ft.TextSpan(text='Refrigerante',style=ft.TextStyle(color=ft.colors.GREEN_600,weight=ft.FontWeight.BOLD,size=25)),
                        ft.TextSpan(text=' De 1 LT',style=ft.TextStyle(color=ft.colors.WHITE,weight=ft.FontWeight.BOLD,size=25)),
                    ]
                ),
                            ft.Text(
                                value='Batata Palha',
                                size=25,
                                color=ft.colors.WHITE,
                                offset=ft.Offset(y=0,x=0.19),
                                weight=ft.FontWeight.BOLD
                            ),
                            ft.Text(
                                value='+Brinde',
                                size=25,
                                color=ft.colors.RED_600,
                                offset=ft.Offset(y=0,x=0.35),
                                weight=ft.FontWeight.BOLD
                            )
                        ]
                    )
                )
            ]
        )
    )
    logo_principal=ft.Container(
        bgcolor=ft.colors.BLACK,
        border_radius=ft.border_radius.all(10),
        alignment=ft.alignment.top_center,
        content=ft.Image(
            src='logo_2.jpeg',
            fit=ft.ImageFit.CONTAIN
        )
    )
    lanches_principal= ft.Container(
        content=ft.Column(
            controls=[
                button_artesanais,
                lanche(nome='hamburguinho',preco='10,00',receita='Pão da Casa, C/Hambúrguer, Tomate, Alface, Molho.'),
                lanche(nome='X-Calabresa',preco='19,99',receita='Pão da Casa, C/Hambúrguer, Calabresa, Queijo, Presunto, Tomate, Alface, Molho.'),
                lanche(nome='X-Bacon',preco='19,99',receita='Pão da Casa, C/Hambúrguer, Bacon, Queijo, Presunto, Tomate, Alface, Molho.'),
                lanche(nome='X-Frangão',preco='19,99',receita='Pão da Casa, C/Hambúrguer, Frango, Queijo, Presunto, Tomate, Alface, Molho.'),
                lanche(nome='X-Mamãe',preco='35,00',receita='Pão da Casa, C/Hambúrguer, Calabresa, Bacon, Frango, Queijo, Presunto, Tomate, Alface, Molho.'),
                adiocionais
            ]
        )
    )
    porcoes = ft.Container(
        content=ft.Column(
            controls=[
               pedido(nome='porções'),
               porcao(nome='Batata Frita C/Bacon',preco='29.99'),
               porcao(nome='Batata Frita C/Calabresa',preco='29.00'),
               porcao(nome='Batata Frita C/Queijo (Cheddar ou Catupiry)',preco='29.99'),
               porcao(nome='Batata Frita Completa',preco='39.99')
            ]
        )
    )
    bebidas = ft.Container(
        content=ft.Column(
            controls=[
                pedido(nome='bebidas'),
                porcao(nome='Copo de Suco',preco='5.99'),
                porcao(nome='Refrigerante Lata',preco='5.99'),
                porcao(nome='Refrigerante 1 LT',preco='9.99'),
                porcao(nome='Refrigerante 2 LT',preco='15.99'),
                porcao(nome='Água 500 ML',preco='3.99'),
                porcao(nome='Água C/Gás 500 ML',preco='4.99')
            ]
        )
    )
    
    page_artesanais = ft.Container(
        bgcolor=ft.colors.BLACK,
        expand=True,
        col={'xs':0,'md':4,'lg':4},
        border_radius=ft.border_radius.all(10),
        content=ft.Column(
            spacing=12,
            scroll=ft.ScrollMode.HIDDEN,
            controls=[
                logo,
                lanches,
                combos,
                footer
            ],
            
        ),
        alignment=ft.alignment.center_left
    )
    page_principal = ft.Container(
        col={'xs':12,'md':4,'lg':4},
        bgcolor=ft.colors.BLACK,
        border_radius=ft.border_radius.all(10),
        alignment=ft.alignment.top_center,
        content=ft.Column(
            spacing=0,
            scroll=ft.ScrollMode.HIDDEN,
            controls=[
                logo_principal,
                lanches_principal,
                porcoes,
                bebidas,
                footer
            ]
        )
    )
    tela_de_pedidos = ft.Container(
        col={'xs':0,'md':4,'lg':4},
        padding=ft.padding.only(right=5),
        bgcolor=ft.colors.BLACK,
        border_radius=ft.border_radius.all(15),
        content=ft.Column(
            scroll=ft.ScrollMode.HIDDEN,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                logo_pedidos,
                button_artesanais,
                nome,
                campo_mesa,
                campo_lanches,
                campo_artesanais,
                campo_combos,
                campo_bebidas,
                campo_porcoes,
                campo_lista,
                total,
                enviar_pedido,
                footer
                
            ]
        )
        )
    
    layout = ft.ResponsiveRow(
        columns=12,
        spacing=0,
        controls=[
            page_principal,
            page_artesanais,
            tela_de_pedidos
        ],expand=True,alignment=ft.alignment.top_center
    )
    page.padding = ft.padding.all(5)
    page.add(layout)
    
if __name__ == '__main__':
    ft.app(target=main,assets_dir='assets')