create schema amnesiabri;

create table amnesiabri.service (
    id      smallserial not null,
    name    smalltext   not null,

    constraint pk_service
        primary key(id)
);

create table amnesiabri.taxa (
    id      smallserial not null,
    name    smalltext   not null,

    constraint pk_taxa
        primary key(id)
);

create table amnesiabri.ecosystem (
    id      smallserial not null,
    name    smalltext   not null,

    constraint pk_ecosystem
        primary key(id)
);

create table amnesiabri.geofocus (
    id      smallserial not null,
    name    smalltext   not null,

    constraint pk_geofocus
        primary key(id)
);

create table amnesiabri.bri (
    content_id  integer not null,
    body        text    not null,
    financial   text,
    url_link    url,
    contact     text,
    logo_id     integer,

    constraint pk_bri
        primary key(content_id),

    constraint fk_content
        foreign key(content_id) references public.content(id),

    constraint fk_file
        foreign key(logo_id) references public.data(content_id)
);

create table amnesiabri.bri_service (
    bri_id      integer     not null,
    service_id  smallint    not null,

    constraint pk_bri_service
        primary key(bri_id, service_id),

    constraint fk_bri_service_bri
        foreign key(bri_id) references amnesiabri.bri(content_id),

    constraint fk_bri_service_service
        foreign key(service_id) references amnesiabri.service(id)
);

create table amnesiabri.bri_taxa (
    bri_id  integer     not null,
    taxa_id smallint    not null,

    constraint pk_bri_taxa
        primary key(bri_id, taxa_id),

    constraint fk_bri_taxa_bri
        foreign key(bri_id) references amnesiabri.bri(content_id),

    constraint fk_bri_taxa_taxa
        foreign key(taxa_id) references amnesiabri.taxa(id)
);

create table amnesiabri.bri_ecosystem (
    bri_id          integer     not null,
    ecosystem_id    smallint    not null,

    constraint pk_bri_ecosystem
        primary key(bri_id, ecosystem_id),

    constraint fk_bri_ecosystem_bri
        foreign key(bri_id) references amnesiabri.bri(content_id),

    constraint fk_bri_ecosystem_ecosystem
        foreign key(ecosystem_id) references amnesiabri.ecosystem(id)
);

create table amnesiabri.bri_geofocus (
    bri_id      integer     not null,
    geofocus_id smallint    not null,

    constraint pk_bri_geofocus
        primary key(bri_id, geofocus_id),

    constraint fk_bri_geofocus_bri
        foreign key(bri_id) references amnesiabri.bri(content_id),

    constraint fk_bri_geofocus_geofocus
        foreign key(geofocus_id) references amnesiabri.geofocus(id)
);

insert into public.content_type(name, icons)
values('bri', '{"fa": "fa-atom"}');

insert into amnesiabri.service(name) values 
('Online databases/data portals/repositories'),
('Collections of specimens or organisms'),
('Research ships, vessels, vehicles'),
('On field/sampling material'),
('Laboratories/on-site platforms'),
('Networking');

insert into amnesiabri.taxa(name) values
('Invertebrates'),
('Vertebrates'),
('Plants'),
('Fungi'),
('Micro-organisms');

insert into amnesiabri.ecosystem(name) values
('Terrestrial'),
('Marine'),
('Freshwater');

insert into amnesiabri.geofocus(name) values
('Wallonia/Flanders/Brussels'),
('National'),
('European'),
('Global/worldwide'),
('Other');
