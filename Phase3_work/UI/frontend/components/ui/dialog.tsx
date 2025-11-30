"use client";

import * as React from "react";
import * as DialogPrimitive from "@radix-ui/react-dialog";
import { XIcon } from "lucide-react";
import { cn } from "./utils";

// -------------------- Root --------------------
const Dialog = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Root>,
  React.ComponentProps<typeof DialogPrimitive.Root>
>((props, ref) => <DialogPrimitive.Root {...props} ref={ref} />);
Dialog.displayName = "Dialog";

// -------------------- Trigger --------------------
const DialogTrigger = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Trigger>,
  React.ComponentProps<typeof DialogPrimitive.Trigger>
>((props, ref) => <DialogPrimitive.Trigger {...props} ref={ref} />);
DialogTrigger.displayName = "DialogTrigger";

// -------------------- Portal --------------------
const DialogPortal = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Portal>,
  React.ComponentProps<typeof DialogPrimitive.Portal>
>((props, ref) => <DialogPrimitive.Portal {...props} ref={ref} />);
DialogPortal.displayName = "DialogPortal";

// -------------------- Close --------------------
const DialogClose = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Close>,
  React.ComponentProps<typeof DialogPrimitive.Close>
>((props, ref) => <DialogPrimitive.Close {...props} ref={ref} />);
DialogClose.displayName = "DialogClose";

// -------------------- Overlay --------------------
const DialogOverlay = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Overlay>,
  React.ComponentProps<typeof DialogPrimitive.Overlay>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Overlay
    className={cn(
      "fixed inset-0 z-50 bg-black/50 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0",
      className
    )}
    {...props}
    ref={ref}
  />
));
DialogOverlay.displayName = "DialogOverlay";

// -------------------- Content --------------------
const DialogContent = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Content>,
  React.ComponentProps<typeof DialogPrimitive.Content>
>(({ className, children, ...props }, ref) => (
  <DialogPortal>
    <DialogOverlay />
    <DialogPrimitive.Content
      className={cn(
        "bg-background fixed top-[50%] left-[50%] z-50 grid w-full max-w-[calc(100%-2rem)] translate-x-[-50%] translate-y-[-50%] gap-4 rounded-lg border p-6 shadow-lg data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95",
        className
      )}
      {...props}
      ref={ref}
    >
      {children}
      <DialogPrimitive.Close className="absolute top-4 right-4 rounded-xs opacity-70 transition-opacity hover:opacity-100 focus:ring-2 focus:ring-offset-2 focus:outline-none [&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4">
        <XIcon />
        <span className="sr-only">Close</span>
      </DialogPrimitive.Close>
    </DialogPrimitive.Content>
  </DialogPortal>
));
DialogContent.displayName = "DialogContent";

// -------------------- Header --------------------
const DialogHeader = React.forwardRef<
  HTMLDivElement,
  React.ComponentProps<"div">
>(({ className, ...props }, ref) => (
  <div
    className={cn("flex flex-col gap-2 text-center sm:text-left", className)}
    {...props}
    ref={ref}
  />
));
DialogHeader.displayName = "DialogHeader";

// -------------------- Footer --------------------
const DialogFooter = React.forwardRef<
  HTMLDivElement,
  React.ComponentProps<"div">
>(({ className, ...props }, ref) => (
  <div
    className={cn(
      "flex flex-col-reverse gap-2 sm:flex-row sm:justify-end",
      className
    )}
    {...props}
    ref={ref}
  />
));
DialogFooter.displayName = "DialogFooter";

// -------------------- Title --------------------
const DialogTitle = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Title>,
  React.ComponentProps<typeof DialogPrimitive.Title>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Title
    className={cn("text-lg leading-none font-semibold", className)}
    {...props}
    ref={ref}
  />
));
DialogTitle.displayName = "DialogTitle";

// -------------------- Description --------------------
const DialogDescription = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Description>,
  React.ComponentProps<typeof DialogPrimitive.Description>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Description
    className={cn("text-muted-foreground text-sm", className)}
    {...props}
    ref={ref}
  />
));
DialogDescription.displayName = "DialogDescription";

// -------------------- Export --------------------
export {
  Dialog,
  DialogTrigger,
  DialogPortal,
  DialogClose,
  DialogOverlay,
  DialogContent,
  DialogHeader,
  DialogFooter,
  DialogTitle,
  DialogDescription,
};
