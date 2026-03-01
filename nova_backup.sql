--
-- PostgreSQL database dump
--

\restrict nqhnRj7rE7aQ4WXEodEg9hZcOzvrx06hb3MH7nCSmAVCW2auNmaWXO0yPN7m4T7

-- Dumped from database version 16.11 (Ubuntu 16.11-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.11 (Ubuntu 16.11-0ubuntu0.24.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: cart; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cart (
    id integer NOT NULL,
    user_id integer NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.cart OWNER TO postgres;

--
-- Name: cart_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cart_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cart_id_seq OWNER TO postgres;

--
-- Name: cart_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cart_id_seq OWNED BY public.cart.id;


--
-- Name: cart_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cart_items (
    id integer NOT NULL,
    cart_id integer NOT NULL,
    product_id bigint NOT NULL,
    quantity integer DEFAULT 1 NOT NULL
);


ALTER TABLE public.cart_items OWNER TO postgres;

--
-- Name: cart_items_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cart_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cart_items_id_seq OWNER TO postgres;

--
-- Name: cart_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cart_items_id_seq OWNED BY public.cart_items.id;


--
-- Name: categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.categories (
    name character varying(255) NOT NULL,
    slug character varying(255) NOT NULL,
    created_at timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.categories OWNER TO postgres;

--
-- Name: categories_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.categories_id_seq OWNER TO postgres;

--
-- Name: categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.categories_id_seq OWNED BY public.categories.id;


--
-- Name: contact_messages; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.contact_messages (
    id character varying(30) NOT NULL,
    name character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    message text NOT NULL,
    is_read boolean DEFAULT false NOT NULL,
    created_at timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public.contact_messages OWNER TO postgres;

--
-- Name: order_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.order_items (
    id integer NOT NULL,
    order_id integer NOT NULL,
    product_id bigint NOT NULL,
    quantity integer NOT NULL,
    price numeric(10,2) NOT NULL
);


ALTER TABLE public.order_items OWNER TO postgres;

--
-- Name: order_items_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.order_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.order_items_id_seq OWNER TO postgres;

--
-- Name: order_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.order_items_id_seq OWNED BY public.order_items.id;


--
-- Name: orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders (
    id integer NOT NULL,
    user_id integer NOT NULL,
    status character varying(50) DEFAULT 'pending'::character varying,
    total numeric(10,2) DEFAULT 0.00 NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.orders OWNER TO postgres;

--
-- Name: orders_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.orders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.orders_id_seq OWNER TO postgres;

--
-- Name: orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.orders_id_seq OWNED BY public.orders.id;


--
-- Name: payments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.payments (
    id integer NOT NULL,
    order_id integer NOT NULL,
    provider character varying(50),
    status character varying(50),
    amount numeric(10,2),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.payments OWNER TO postgres;

--
-- Name: payments_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.payments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.payments_id_seq OWNER TO postgres;

--
-- Name: payments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.payments_id_seq OWNED BY public.payments.id;


--
-- Name: products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.products (
    name character varying(255) NOT NULL,
    slug character varying(255) NOT NULL,
    description text NOT NULL,
    price double precision,
    image_url character varying(500) NOT NULL,
    category_id integer NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    id bigint NOT NULL,
    stok integer
);


ALTER TABLE public.products OWNER TO postgres;

--
-- Name: products_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.products ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.products_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: services; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.services (
    title character varying(255) NOT NULL,
    slug character varying(255) NOT NULL,
    description text NOT NULL,
    icon character varying(255) NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    id bigint NOT NULL,
    price character varying(100),
    short_description character varying(500),
    features jsonb
);


ALTER TABLE public.services OWNER TO postgres;

--
-- Name: services_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.services ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.services_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    email character varying(255) NOT NULL,
    password character varying(255) NOT NULL,
    role_id smallint DEFAULT 1 NOT NULL,
    created_at timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: cart id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart ALTER COLUMN id SET DEFAULT nextval('public.cart_id_seq'::regclass);


--
-- Name: cart_items id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart_items ALTER COLUMN id SET DEFAULT nextval('public.cart_items_id_seq'::regclass);


--
-- Name: categories id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories ALTER COLUMN id SET DEFAULT nextval('public.categories_id_seq'::regclass);


--
-- Name: order_items id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items ALTER COLUMN id SET DEFAULT nextval('public.order_items_id_seq'::regclass);


--
-- Name: orders id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);


--
-- Name: payments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments ALTER COLUMN id SET DEFAULT nextval('public.payments_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: cart; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cart (id, user_id, created_at, updated_at) FROM stdin;
1	1	2026-02-27 18:50:47.92802	2026-02-27 18:50:47.92802
2	2	2026-02-27 18:50:47.92802	2026-02-27 18:50:47.92802
\.


--
-- Data for Name: cart_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cart_items (id, cart_id, product_id, quantity) FROM stdin;
7	1	13	2
8	1	14	1
9	2	15	1
\.


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.categories (name, slug, created_at, updated_at, id) FROM stdin;
Audífonos	audifonos	2026-02-19 12:28:10.842	2026-02-19 12:28:10.842	1
Cargadores	cargadores	2026-02-19 12:28:10.842	2026-02-19 12:28:10.842	2
Power Banks	power-banks	2026-02-19 12:28:10.842	2026-02-19 12:28:10.842	3
\.


--
-- Data for Name: contact_messages; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.contact_messages (id, name, email, message, is_read, created_at) FROM stdin;
\.


--
-- Data for Name: order_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.order_items (id, order_id, product_id, quantity, price) FROM stdin;
4	1	13	2	120000.00
5	1	14	1	80000.00
6	2	15	1	150000.00
\.


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orders (id, user_id, status, total, created_at) FROM stdin;
1	1	paid	320000.00	2026-02-27 18:54:58.920767
2	2	pending	150000.00	2026-02-27 18:54:58.920767
\.


--
-- Data for Name: payments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.payments (id, order_id, provider, status, amount, created_at) FROM stdin;
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.products (name, slug, description, price, image_url, category_id, is_active, created_at, updated_at, id, stok) FROM stdin;
UGREEN Nexode 140W GaN Charger	ugreen-nexode-140w-gan	Cargador USB-C 140W con tecnología GaN avanzada. Carga MacBook Pro 16 en 40 minutos. 2 puertos USB-C simultáneos. Compacto y premium.	89.99	https://via.placeholder.com/500x500?text=UGREEN+140W+Charger	2	t	2026-02-19 12:29:45.323	2026-02-19 12:29:45.323	14	10
UGREEN USB-C Hub 12 in 1	ugreen-usb-hub-12in1	Hub USB-C 12 puertos - 4K HDMI, USB 3.0, SD, Ethernet, PD 100W. Convierte tu laptop en workstation profesional. Compatible con MacBook y Windows.	129.99	https://via.placeholder.com/500x500?text=USB-C+Hub+12in1	2	t	2026-02-19 12:29:45.323	2026-02-19 12:29:45.323	15	10
UGREEN Lightning Cable 2M (3-pack)	ugreen-lightning-cable-3pack	Cables Lightning certificados MFi. 3 unidades de 2 metros. Carga y transferencia rápida. Durabilidad garantizada. Perfectos para oficina, hogar, carro.	34.99	https://via.placeholder.com/500x500?text=Lightning+Cable+3Pack	2	t	2026-02-19 12:29:45.323	2026-02-19 12:29:45.323	16	10
UGREEN 65W Car Charger Dual USB-C	ugreen-65w-car-charger-dual-usbc	Cargador para auto con 2 puertos USB-C y salida total 65W. Compatible con carga rápida PD y QC. Carga laptop y teléfono a la vez.	29.99	https://via.placeholder.com/500x500?text=Car+Charger+65W	2	t	2026-02-19 12:29:45.323	2026-02-19 12:29:45.323	17	10
UGREEN USB-C Cable 240W (2m)	ugreen-usbc-cable-240w-2m	Cable USB-C certificado para hasta 240W (PD 3.1). Ideal para laptops y estaciones de trabajo. Trenzado, resistente y confiable.	19.99	https://via.placeholder.com/500x500?text=USB-C+Cable+240W	2	t	2026-02-19 12:29:45.323	2026-02-19 12:29:45.323	18	10
UGREEN Power Bank 25000mAh 65W	ugreen-power-bank-25000	Power bank 25000mAh con carga rápida 65W. Carga tu iPhone 15 7 veces. USB-C entrada/salida. Display digital. Ultra rápido y confiable.	79.99	https://via.placeholder.com/500x500?text=PowerBank+25000mAh	3	t	2026-02-19 12:29:45.323	2026-02-19 12:29:45.323	19	10
UGREEN MagSafe Power Bank 10000mAh	ugreen-magsafe-power-bank-10000	Power bank magnético 10000mAh compatible con MagSafe. Carga inalámbrica 15W y USB-C 20W. Diseño compacto, ideal para iPhone y viajes.	59.99	https://via.placeholder.com/500x500?text=MagSafe+PowerBank+10000	3	t	2026-02-19 12:29:45.323	2026-02-19 12:29:45.323	20	10
UGREEN Power Bank 20000mAh 100W	ugreen-power-bank-20000-100w	Power bank 20000mAh con salida 100W y 2x USB-C. Carga MacBook, Steam Deck y más. Pantalla digital y múltiples protecciones.	99.99	https://via.placeholder.com/500x500?text=PowerBank+20000mAh	3	t	2026-02-19 12:29:45.323	2026-02-19 12:29:45.323	21	10
UGREEN Wireless Earbuds T8 Pro	ugreen-wireless-earbuds-t8	Audífonos inalámbricos con cancelación activa de ruido (ANC). Batería 10 horas. Conexión estable Bluetooth 5.3. Diseño ergonómico premium.	199.99	https://via.placeholder.com/500x500?text=Earbuds+T8+Pro	1	t	2026-02-19 12:29:45.323	2026-02-19 12:29:45.323	22	10
UGREEN AirLite ANC Headphones	ugreen-airlite-anc-headphones	Audífonos over-ear con ANC híbrido y 60 horas de batería. Sonido Hi-Res, modo transparencia y comodidad premium para largas jornadas.	149.99	https://via.placeholder.com/500x500?text=AirLite+ANC+Headphones	1	t	2026-02-19 12:29:45.323	2026-02-19 12:29:45.323	23	10
UGREEN Spark Buds Mini	ugreen-spark-buds-mini	Audífonos compactos con estuche ultraligero. Sonido balanceado, 30 horas con estuche y modo gaming de baja latencia.	49.99	https://via.placeholder.com/500x500?text=Spark+Buds+Mini	1	t	2026-02-19 12:29:45.323	2026-02-19 12:29:45.323	24	10
UGREEN Nexode 300W GaN Charger	ugreen-nexode-300w-gan	Cargador GaN de 300W con 6 puertos - el más potente del mercado. Carga 3 laptops simultáneamente. USB-C 140W, 2x USB-C 65W, 3x USB-A. Perfecto para profesionales.	249.99	https://via.placeholder.com/500x500?text=UGREEN+300W+Charger	2	t	2026-02-19 12:29:45.323	2026-02-19 12:29:45.323	13	10
Producto con stok	Stok.com	producto que contiene stok	500	stok.jpeg	2	t	2026-02-23 09:25:40.289	2026-02-23 09:25:40.289	26	3
\.


--
-- Data for Name: services; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.services (title, slug, description, icon, is_active, created_at, updated_at, id, price, short_description, features) FROM stdin;
Desarrollo de Páginas Web	desarrollo-paginas-web	Creamos sitios web modernos, responsivos y optimizados para SEO. Desde landing pages hasta portales corporativos completos con las últimas tecnologías.	globe	t	2026-02-18 21:32:08.761	2026-02-18 21:32:08.761	11	Desde $500	Sitios web profesionales y optimizados para tu negocio	["Diseño responsive", "Optimización SEO", "Panel de administración", "Integración con redes sociales", "Hosting y dominio incluido", "Mantenimiento mensual"]
Aplicaciones Móviles	aplicaciones-moviles	Desarrollamos apps nativas y multiplataforma para iOS y Android. Soluciones móviles que conectan tu negocio con tus clientes de manera directa y efectiva.	smartphone	t	2026-02-18 21:32:08.761	2026-02-18 21:32:08.761	12	Desde $2,000	Apps móviles nativas y multiplataforma para tu empresa	["Desarrollo iOS y Android", "Diseño UX/UI profesional", "Push notifications", "Integración con APIs", "Publicación en tiendas", "Soporte post-lanzamiento"]
Sistemas de Inventario	sistemas-inventario	Sistemas de gestión de inventario personalizados para optimizar el control de stock, productos y almacenes. Incluye reportes en tiempo real y alertas automáticas.	package	t	2026-02-18 21:32:08.761	2026-02-18 21:32:08.761	13	Desde $1,500	Control total de tu inventario con reportes en tiempo real	["Control de stock en tiempo real", "Gestión de múltiples almacenes", "Códigos de barras/QR", "Reportes y estadísticas", "Alertas de stock mínimo", "Integración con facturación"]
Modelos de Inteligencia Artificial	modelos-ia	Desarrollamos e implementamos modelos de IA personalizados: machine learning, análisis predictivo, chatbots inteligentes, reconocimiento de patrones y automatización con IA.	cpu	t	2026-02-18 21:32:08.761	2026-02-18 21:32:08.761	14	Desde $3,000	Soluciones de IA para automatizar y optimizar tu negocio	["Análisis predictivo", "Chatbots inteligentes", "Procesamiento de lenguaje natural", "Reconocimiento de imágenes", "Automatización de procesos", "Integración con sistemas existentes"]
Sistemas ERP Empresariales	sistemas-erp	Soluciones ERP completas para gestionar todos los procesos de tu empresa: ventas, compras, inventario, finanzas, recursos humanos y más, todo en una plataforma integrada.	building	t	2026-02-18 21:32:08.761	2026-02-18 21:32:08.761	15	Desde $4,000	Sistema integral para gestionar toda tu empresa	["Gestión de ventas y compras", "Control financiero", "Recursos humanos", "Reportes ejecutivos", "Facturación electrónica", "Multi-empresa y multi-moneda"]
E-commerce y Tiendas Online	ecommerce-tiendas	Tiendas online completas con carrito de compras, pasarelas de pago, gestión de productos y pedidos. Aumenta tus ventas llevando tu negocio al mundo digital.	shopping-cart	t	2026-02-18 21:32:08.761	2026-02-18 21:32:08.761	16	Desde $1,800	Vende online con tu propia tienda virtual	["Catálogo de productos ilimitado", "Múltiples métodos de pago", "Gestión de envíos", "Panel de administración", "Marketing y cupones", "Integración con redes sociales"]
Sistemas CRM	sistemas-crm	Software CRM para gestionar relaciones con clientes, seguimiento de ventas, automatización de marketing y análisis del embudo de conversión para aumentar tus ventas.	users	t	2026-02-18 21:32:08.761	2026-02-18 21:32:08.761	17	Desde $2,500	Gestiona tus clientes y aumenta tus ventas	["Gestión de contactos y leads", "Seguimiento de oportunidades", "Automatización de emails", "Reportes de ventas", "Pipeline visual", "Integración con WhatsApp"]
Aplicaciones Web Personalizadas	aplicaciones-web	Desarrollo de aplicaciones web a medida según las necesidades específicas de tu negocio. Sistemas complejos, portales, dashboards y más.	monitor	t	2026-02-18 21:32:08.761	2026-02-18 21:32:08.761	18	Desde $2,000	Soluciones web a medida para necesidades específicas	["Arquitectura escalable", "Múltiples usuarios y roles", "API REST integrada", "Seguridad avanzada", "Dashboards interactivos", "Integración con terceros"]
Automatización de Procesos	automatizacion-procesos	Automatizamos procesos repetitivos de tu empresa mediante scripts, integraciones y bots. Ahorra tiempo y reduce errores humanos con automatización inteligente.	zap	t	2026-02-18 21:32:08.761	2026-02-18 21:32:08.761	19	Desde $1,000	Automatiza tareas repetitivas y ahorra tiempo	["Integración entre sistemas", "Bots de automatización", "Procesamiento de documentos", "Notificaciones automáticas", "Reportes programados", "API personalizadas"]
Consultoría y Soporte Técnico	consultoria-soporte	Asesoría técnica especializada, auditoría de sistemas, optimización de infraestructura, soporte técnico continuo y capacitación para tu equipo.	headphones	t	2026-02-18 21:32:08.761	2026-02-18 21:32:08.761	20	Desde $100/hora	Asesoría experta para tus proyectos tecnológicos	["Auditoría de sistemas", "Optimización de performance", "Seguridad informática", "Migración de sistemas", "Capacitación de equipos", "Soporte técnico 24/7"]
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, name, email, password, role_id, created_at) FROM stdin;
1	Julian Ordóñez	julian@nova.com	hashed_password_123	1	2026-02-27 18:50:34.897
2	Maria Lopez	maria@gmail.com	hashed_password_456	1	2026-02-27 18:50:34.897
3	Carlos Perez	carlos@gmail.com	hashed_password_789	1	2026-02-27 18:50:34.897
\.


--
-- Name: cart_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cart_id_seq', 2, true);


--
-- Name: cart_items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cart_items_id_seq', 9, true);


--
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.categories_id_seq', 4, true);


--
-- Name: order_items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.order_items_id_seq', 6, true);


--
-- Name: orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.orders_id_seq', 2, true);


--
-- Name: payments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.payments_id_seq', 1, false);


--
-- Name: products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.products_id_seq', 26, true);


--
-- Name: services_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.services_id_seq', 21, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 3, true);


--
-- Name: cart_items cart_items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT cart_items_pkey PRIMARY KEY (id);


--
-- Name: cart cart_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart
    ADD CONSTRAINT cart_pkey PRIMARY KEY (id);


--
-- Name: cart cart_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart
    ADD CONSTRAINT cart_user_id_key UNIQUE (user_id);


--
-- Name: categories categories_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_name_key UNIQUE (name);


--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- Name: categories categories_slug_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_slug_key UNIQUE (slug);


--
-- Name: contact_messages contact_messages_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contact_messages
    ADD CONSTRAINT contact_messages_pkey PRIMARY KEY (id);


--
-- Name: order_items order_items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_pkey PRIMARY KEY (id);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- Name: payments payments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_pkey PRIMARY KEY (id);


--
-- Name: products products_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_name_key UNIQUE (name);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- Name: products products_slug_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_slug_key UNIQUE (slug);


--
-- Name: services services_slug_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.services
    ADD CONSTRAINT services_slug_key UNIQUE (slug);


--
-- Name: services services_title_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.services
    ADD CONSTRAINT services_title_key UNIQUE (title);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: idx_categories_slug; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_categories_slug ON public.categories USING btree (slug);


--
-- Name: idx_contact_messages_created_at; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_contact_messages_created_at ON public.contact_messages USING btree (created_at);


--
-- Name: idx_contact_messages_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_contact_messages_email ON public.contact_messages USING btree (email);


--
-- Name: idx_products_category_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_products_category_id ON public.products USING btree (category_id);


--
-- Name: idx_products_slug; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_products_slug ON public.products USING btree (slug);


--
-- Name: idx_services_slug; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_services_slug ON public.services USING btree (slug);


--
-- Name: products Product_categoryId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT "Product_categoryId_fkey" FOREIGN KEY (category_id) REFERENCES public.categories(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: cart_items cart_items_cart_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT cart_items_cart_id_fkey FOREIGN KEY (cart_id) REFERENCES public.cart(id) ON DELETE CASCADE;


--
-- Name: cart_items cart_items_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT cart_items_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- Name: cart cart_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart
    ADD CONSTRAINT cart_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: order_items order_items_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id) ON DELETE CASCADE;


--
-- Name: order_items order_items_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- Name: orders orders_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: payments payments_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict nqhnRj7rE7aQ4WXEodEg9hZcOzvrx06hb3MH7nCSmAVCW2auNmaWXO0yPN7m4T7

