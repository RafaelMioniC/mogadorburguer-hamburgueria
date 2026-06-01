create database hamburgueria;
use hamburgueria;

create table cliente(
cliente_id int primary key auto_increment,
cliente_nome varchar(30),
cliente_cep varchar(10)
);

create table lanches(
lanche_id int primary key auto_increment,
lanche_nome varchar(30),
lanche_preco decimal(4,2)
);

create table pedido(
pedido_id int primary key auto_increment,
cliente_id int,
lanche_id int,
pedido_preco decimal(8,2)
);

CREATE TABLE pedido_item (
    pedido_item_id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT NOT NULL,
    lanche_id INT NOT NULL,
    item_quantidade INT NOT NULL,

    FOREIGN KEY (pedido_id)
        REFERENCES pedido(pedido_id),

    FOREIGN KEY (lanche_id)
        REFERENCES lanches(lanche_id)
);


create user 'local'@'localhost' identified by 'mogadorburguer';

GRANT ALL PRIVILEGES
ON hamburgueria.*
TO 'local'@'localhost';
FLUSH PRIVILEGES;

insert into lanches(lanche_nome,lanche_preco)
values('Cheese Burguer',30.00),
('Smash Burguer',30.00),
('Duplo Cheddar',40.00),
('Batata Frita',14.00),
('Onion Ring',16.00),
('Mini Churros',11.00),
('Macarons',14.00),
('Petit Gateu',18.00);


ALTER TABLE pedido
ADD CONSTRAINT fk_cliente
FOREIGN KEY (cliente_id)
REFERENCES cliente(cliente_id);

alter table pedido
add column ped_meio varchar(30);



alter table pedido
drop column lanche_id;

select * from pedido;
select * from cliente;

SELECT
    c.cliente_nome,
    p.pedido_preco,
    GROUP_CONCAT(
        CONCAT(l.lanche_nome, ' (', pi.item_quantidade, 'x)')
        SEPARATOR ', '
    ) AS lanches
FROM cliente c
INNER JOIN pedido p
    ON p.cliente_id = c.cliente_id
INNER JOIN pedido_item pi
    ON pi.pedido_id = p.pedido_id
INNER JOIN lanches l
    ON l.lanche_id = pi.lanche_id
GROUP BY
    p.pedido_id,
    c.cliente_nome,
    p.pedido_preco;

SELECT *
FROM lanches;


